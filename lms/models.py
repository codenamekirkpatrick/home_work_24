from django.db import models

from lms.utils import NULLABLE
from users.models import User


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        verbose_name="Превью курса",
        **NULLABLE,
        help_text="Загрузите превью курса"
    )
    description = models.TextField(
        verbose_name="Описание курса", **NULLABLE, help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Владелец",
        related_name="course"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", **NULLABLE, help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lessons_previews/",
        verbose_name="Превью урока",
        **NULLABLE,
        help_text="Загрузите превью урока"
    )
    video_url = models.URLField(verbose_name="Видеоурок", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = (
            "name",
            "course",
        )
