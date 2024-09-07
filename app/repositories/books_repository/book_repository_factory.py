from utils.config import Config
from .mock_repository import MockRepository
from .google_books_repository import GoogleBooksRepository


class BooksRepositoryFactory:
    @staticmethod
    def get_repository():
        if Config.mock_books_responses:
            return MockRepository()
        else:
            return GoogleBooksRepository()
