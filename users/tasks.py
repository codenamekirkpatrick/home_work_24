from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def check_inactive_users():
    """
    Проверяет и деактивирует пользователей, которые не заходили в систему в течение 30 дней.
    """
    User = get_user_model()
    inactive_users = User.objects.filter(
        last_login__lte=timezone.now() - timedelta(days=30), is_active=True
    )
    for user in inactive_users:
        user.is_active = False
        user.save()