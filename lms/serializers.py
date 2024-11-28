from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import YouTubeValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор модели Урок"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeValidator(field="video_url")]


class CourseSerializer(ModelSerializer):
    """Сериализатор модели Курс"""

    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    is_subscription = SerializerMethodField()


    class Meta:
        model = Course
        fields = "__all__"

    def get_total_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscription(self, course):
        user = self.context["request"].user
        subscription = Subscription.objects.filter(course=course.id, user=user.id)
        if subscription:
            return True
        return False




class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для добавления количества уроков одного курса"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    # subscription = SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
