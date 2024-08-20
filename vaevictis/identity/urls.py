from django.urls import path
from .views import LoginAPIView, TestAuthView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("test/", TestAuthView.as_view(), name="test-auth"),
]
