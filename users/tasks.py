from celery import shared_task
from datetime import timezone
from users.models import User
from dateutil.relativedelta import relativedelta

@shared_task
def check_last_login() -> None:
    """
    Проверяет и деактивирует пользователей,
    которые не заходили в систему в течение 1 месяца
    и делает их аккаунт неактивным.
    """
    month_ago = timezone.now() - relativedelta(months=1)
    users = User.objects.filter(last_login__lte=month_ago, is_active=True)
    users.update(is_active=False)