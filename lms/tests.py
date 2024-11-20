from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@test1.com", password="1234")
        self.course = Course.objects.create(name="Test1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        video_url = reverse("lms:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(video_url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        user2 = User.objects.create(email="test2@test2.com", password="1234")
        course2 = Course.objects.create(name="Test2", owner=user2)
        video_url = reverse("lms:lesson-create")
        data = {"name": "Test2", "course": course2.pk, "owner": user2.pk}
        response = self.client.post(video_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        video_url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {
            "name": "Python",
        }
        response = self.client.patch(video_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Python")

    def test_lesson_delete(self):
        video_url = reverse("lms:lesson-destroy", args=(self.lesson.pk,))
        response = self.client.delete(video_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        video_url = reverse("lms:lesson-list")
        response = self.client.get(video_url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "Test1",
                    "description": None,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.com", password="1234")
        self.course = Course.objects.create(name="Java", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        video_url = reverse("lms:subscription-create")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(video_url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(data, {"message": "Подписка создана"})

    def test_subscription_delete(self):
        video_url = reverse("lms:subscription-create")
        data = {
            "course": self.course.pk,
        }
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(video_url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(data, {"message": "Подписка удалена"})
