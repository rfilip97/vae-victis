from django.urls import path
from .views import LoginAPIView, TestAuthView, RegisterAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("test/", TestAuthView.as_view(), name="test-auth"),
]
