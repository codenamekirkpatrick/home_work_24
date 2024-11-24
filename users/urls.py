from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (

    UserCreateAPIView,
    UserDestroyAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView, PaymentCreateAPIView, PaymentListAPIView,
)

app_name = UsersConfig.name

router = SimpleRouter()




urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "users/<int:pk>/retrieve/", UserRetrieveAPIView.as_view(), name="users_retrieve"
    ),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path("users/<int:pk>/destroy/", UserDestroyAPIView.as_view(), name="users_destroy"),
    path(
        "payment-create/", PaymentCreateAPIView.as_view(), name="payment_create"
    ),
    path(
        "payment/", PaymentListAPIView.as_view(), name="payment-list"),
]

urlpatterns += router.urls
