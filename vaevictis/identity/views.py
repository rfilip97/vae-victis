from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "CSRF cookie set"}, status=status.HTTP_200_OK)
