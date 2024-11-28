
import smtplib
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


def send_mailing(address, subject, body):
    """Функция отправки письма"""
    try:
        response = send_mail(
            subject=subject,
            message=body,
            from_email=EMAIL_HOST_USER,
            recipient_list=address,
            fail_silently=False,
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException