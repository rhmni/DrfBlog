from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .manager import UserManager
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150)
    avatar = models.ImageField(default='default_avatar.jpg')
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

    send_mail(
        "Password Reset",
        email_plaintext_message,
        "noreply@host.com",
        [reset_password_token.user.email]
    )
