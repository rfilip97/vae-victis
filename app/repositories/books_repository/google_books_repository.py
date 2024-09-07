import requests
import os
from utils.config import Config
from .i_book_repository import IBooksRepository


class GoogleBooksRepository(IBooksRepository):
    def get_book_info(self, isbn):
        api_key = os.getenv("BOOKS_API_KEY")
        url = f"{Config.books_api_url}/books/v1/volumes?q=ISBN:{isbn}"
        headers = {"x-goog-api-key": api_key}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Error fetching data from Google Books API: {response.status_code}"
            )
