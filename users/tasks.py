from celery import shared_task
from datetime import timedelta, date
from users.models import User


@shared_task
def check_last_login():
    """
    Проверяет и деактивирует пользователей, которые не заходили в систему в течение 30 дней.
    """
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    date_delta = timedelta(30)
    for user in users:
        date_block = date.today() - date_delta
        if user.last_login <= date_block:
            print("Пользователь не активен")
            user.is_active = False
            user.save()