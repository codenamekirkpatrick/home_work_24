from django.contrib import admin
from lms.models import Course, Lesson
from users.models import User, Payment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "preview",
        "description",
        "owner",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "preview",
        "description",
        "owner",
    )
    list_display = (
        "id",
        "name",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = (
        "email",
        "phone",
        "city",
        "avatar",
    )
    list_display = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = (
        "user",
        "date",
        "course",
        "lesson",
        "amount",
        "method",
    )
    list_display = (
        "user",
        "amount",
        "method",
    )
