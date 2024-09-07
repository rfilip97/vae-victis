from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
import json
from .mocked_responses import STUBBED_GOOGLE_BOOKS_RESPONSE


class ScanTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    @patch("requests.get")
    def test_scan_books_view_with_mocked_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = STUBBED_GOOGLE_BOOKS_RESPONSE

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.get(reverse("scan_book"), {"isbn": "9786067580648"})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content), STUBBED_GOOGLE_BOOKS_RESPONSE)
