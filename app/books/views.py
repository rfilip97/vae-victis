import os
import requests
from django.http import JsonResponse


def scan_book(request):
    isbn = request.GET.get("isbn", None)

    if isbn:
        api_key = os.getenv("BOOKS_API_KEY")

        url = f"https://www.googleapis.com/books/v1/volumes?q=ISBN:{isbn}"

        headers = {"x-goog-api-key": api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse(
                {"error": "Error fetching book data from Google Books API"},
                status=response.status_code,
            )
    else:
        return JsonResponse({"error": "ISBN not provided"}, status=400)
