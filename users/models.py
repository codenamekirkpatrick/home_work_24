from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)
    phone = models.CharField(
        max_length=10,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=150, verbose_name="Город", **NULLABLE, help_text="Введите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


from lms.models import Course, Lesson


class Payment(models.Model):
    """Модель платежей"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Кто произвел оплату"
    )
    date = models.DateField(verbose_name="Дата оплаты", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок"
    )
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")
    CASH = "cash"
    TRANSFER = "transfer"
    PAYMENT_METHOD = [(CASH, "cash"), (TRANSFER, "transfer")]
    method = models.CharField(
        choices=PAYMENT_METHOD, default=CASH, verbose_name="Способ оплаты"
    )

    def __str__(self):
        return f"{self.amount} {self.method}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
