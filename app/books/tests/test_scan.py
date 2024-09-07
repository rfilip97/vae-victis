from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
import json
from .mocked_responses import STUBBED_GOOGLE_BOOKS_RESPONSE
from books.models import Book


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

        expected_response = {
            "isbn": "9786067580648",
            "title": "Dune   - Editura Nemira",
            "author": "Frank Herbert",
            "thumbnail": "http://books.google.com/books/content?id=kL_KDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        }

        response = self.client.get(reverse("scan_book"), {"isbn": "9786067580648"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(Book.objects.count(), 1)
        book_in_db = Book.objects.get(isbn="9786067580648")
        self.assertEqual(book_in_db.title, expected_response["title"])

        response = self.client.get(reverse("scan_book"), {"isbn": "9786067580648"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
        self.assertEqual(Book.objects.count(), 1)
