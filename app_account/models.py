from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from app_account.celery_tasks import send_password_reset_mail
from .manager import UserManager
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


def phone_validate(value):
    if len(value) != 11:
        raise ValidationError('phone must be 11 character')
    if not value.isnumeric():
        raise ValidationError('phone must be only number')
    if not value.startswith('09'):
        raise ValidationError('phone must start with "09"')


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    avatar = models.ImageField(default='default_avatar.jpg')
    phone = models.CharField(max_length=20, unique=True, validators=[phone_validate], null=True, blank=True)
    is_phone_Confirm = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser


# this signal for send email reset password
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = f"your token is = {reset_password_token.key}"

    mail_info = {
        'subject': 'Password Reset',
        'message': email_plaintext_message,
        'from_email': 'noreply@host.com',
        'recipient_list': [reset_password_token.user.email],
    }
    send_password_reset_mail.delay(mail_info)
