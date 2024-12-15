from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from lms.models import Course, Subscription




# @shared_task
# def mailing(course_pk):
#     email_list = []
#     course = Course.objects.get(pk=course_pk)
#     subs = Subscription.objects.filter(course=course)
#     for sub in subs:
#         email_list.append(sub.user.email)
#     subject_mail = f"Обновление курса {course.name}"
#     text_mail = (f"Добрый день, в курсе {course.name} произошли изменения.")
#     send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, email_list, fail_silently=True)
#     print("Письмо отправленно")


@shared_task
def mailing(course_pk: int) -> None:
    course = Course.objects.get(pk=course_pk)

    course_subscriptions = Subscription.objects.filter(course=course)
    email_list = course_subscriptions.values_list('user__email', flat=True)

    subject_mail = f"Обновление курса {course.name}"
    text_mail = f"Добрый день, в курсе {course.name} произошли изменения."
    send_mail(
        subject_mail,
        text_mail,
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False
    )