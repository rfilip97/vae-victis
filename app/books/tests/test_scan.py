import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .mocked_responses import STUBBED_GOOGLE_BOOKS_RESPONSE


class ScanTest(TestCase):
    @patch("requests.get")
    def test_scan_books_view_with_mocked_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = STUBBED_GOOGLE_BOOKS_RESPONSE

        response = self.client.get(reverse("scan_book"), {"isbn": "9786067580648"})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content), STUBBED_GOOGLE_BOOKS_RESPONSE)
