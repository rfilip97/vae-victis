from django.urls import path
from .views import LoginAPIView, TestAuthView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("test/", TestAuthView.as_view(), name="test_auth"),
]
