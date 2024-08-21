from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer


class LoginAPIView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class TestAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {"message": f"You are logged in, {request.user.username}"},
            status=status.HTTP_200_OK,
        )
