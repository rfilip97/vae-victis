from .i_book_repository import IBooksRepository
from books.tests.mocked_responses import STUBBED_GOOGLE_BOOKS_RESPONSE


class MockRepository(IBooksRepository):
    def get_book_info(self, isbn):

        return STUBBED_GOOGLE_BOOKS_RESPONSE
