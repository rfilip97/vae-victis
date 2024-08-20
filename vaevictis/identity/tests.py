from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status


class TestAuthViewTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.client = APIClient()
        self.test_url = reverse("test-auth")

    def test_auth_view_authenticated(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"message": f"You are logged in, {self.username}"}
        )

    def test_auth_view_unauthenticated(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LoginAPIViewTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.client = APIClient()
        self.login_url = reverse("login")

    def test_login_with_valid_credentials(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Login successful"})

    def test_login_with_invalid_credentials(self):
        data = {"username": self.username, "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"non_field_errors": ["Invalid login credentials."]}
        )

    def test_login_with_missing_fields(self):
        data = {"username": self.username}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_login_with_disabled_user(self):
        self.user.is_active = False
        self.user.save()

        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"non_field_errors": ["User account is disabled."]}
        )
