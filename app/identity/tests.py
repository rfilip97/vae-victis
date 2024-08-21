from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserAuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.test_auth_url = reverse("test_auth")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_duplicate_username_registration(self):
        duplicate_user_data = {
            "username": "testuser",
            "password": "newpassword",
            "password2": "newpassword",
            "email": "duplicate@example.com",
        }
        response = self.client.post(
            self.register_url, duplicate_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration(self):
        new_user_data = {
            "username": "newtestuser",
            "password": "newtestpassword",
            "password2": "newtestpassword",
            "email": "newtest@example.com",
        }
        response = self.client.post(self.register_url, new_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_access_protected_view_with_valid_token(self):
        login_data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]

        response = self.client.get(
            self.test_auth_url, HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "You are logged in, testuser")

    def test_access_protected_view_with_invalid_token(self):
        response = self.client.get(self.test_auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            self.test_auth_url, HTTP_AUTHORIZATION="Bearer invalidtoken"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
