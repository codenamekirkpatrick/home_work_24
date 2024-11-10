from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор модели Урок"""
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор модели Курс"""
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для добавления количества уроков одного курса"""
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Lesson
        fields = (
            "name",
            "description",
            "preview",
            "course",
            "lessons_count",
            "lessons"
        )






