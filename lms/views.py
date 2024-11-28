from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from lms.models import Course, Lesson, Subscription
from lms.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from users.permissions import IsModer, IsOwner
from rest_framework.response import Response
from lms.paginations import CustomPagination
from lms.tasks import mailing_about_updates


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsAuthenticated,)
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = (IsAuthenticated | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Функция автоматического сохранения владельца."""
        course = serializer.save()
        course.owner = self.request.user
        course.save()


    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)



class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Функция автоматического сохранения владельца."""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]




class SubscriptionCreateAPIView(CreateAPIView):
    """Эндпоинт на создание и удаление подписки"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """Реализация создания и удаления подписки через метод post"""
        user = self.request.user
        # id курса, которое передал пользователь
        course_id = self.request.data.get("course")
        # сущность курса, все данные по курсу, который запросил пользователь
        course_item = get_object_or_404(Course, pk=course_id)
        # queryset на сущность подписки фильтр по вошедшему пользователю и курсу
        subs_item = Subscription.objects.filter(course=course_item, user=user)

        if subs_item.exists():  #  если такая подписка существует то удаляем
            subs_item.delete()
            message = "Подписка удалена"
        else:  #  иначе создаем
            Subscription.objects.create(course=course_item, user=user)
            message = "Подписка создана"

        return Response({"message": message})


class SubscriptionListAPIView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
