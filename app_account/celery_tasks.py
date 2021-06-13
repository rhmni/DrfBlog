from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from app_account.models import User


@shared_task
def send_birthday_email():
    users = User.objects.filter(is_active=True, date_of_birth__isnull=False, email__isnull=False)
    time = datetime.today()
    for user in users:
        if user.date_of_birth.day == time.day and user.date_of_birth.month == time.month:
            send_mail(
                f'happy birthday',
                f'Happy birthday, dear {user.name}, have a good year',
                'local@host.com',
                [user.email],
            )
