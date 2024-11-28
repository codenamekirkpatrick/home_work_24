from celery import shared_task
from lms.models import Course
from lms.services import send_mailing


@shared_task
def mailing_about_updates(course_id):
    """Функция отправления сообщений об обновлении курса."""
    course = Course.objects.get(pk=course_id)
    subscription_list = course.subscription.all()
    user_list = [subscription.user for subscription in subscription_list]
    subject = 'Обновление'
    body = f'Вышло обновление по курсу {course}'
    send_mailing(user_list, subject, body)

