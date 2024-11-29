from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from lms.models import Course, Subscription


# @shared_task
# def mailing_about_updates(course_id):
#     """Функция отправления сообщений об обновлении курса."""
#     course = Course.objects.get(pk=course_id)
#     subscription_list = course.subscription.all()
#     user_list = [subscription.user for subscription in subscription_list]
#     subject = 'Обновление'
#     body = f'Вышло обновление по курсу {course}'
#     send_mailing(user_list, subject, body)

@shared_task
def mailing(course_pk):
    email_list = []
    course = Course.objects.get(pk=course_pk)
    subs = Subscription.objects.filter(course=course)
    for sub in subs:
        email_list.append(sub.user.email)
    subject_mail = f"Обновление курса {course.name}"
    text_mail = (f"Добрый день, в курсе {course.name} произошли изменения.")
    send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, email_list, fail_silently=True)
    print("Письмо отправленно")