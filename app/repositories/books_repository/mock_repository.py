from .i_book_repository import IBooksRepository
from books.tests.mocked_responses import STUBBED_GOOGLE_BOOKS_RESPONSE


class MockRepository(IBooksRepository):
    def get_book_info(self, isbn):
        mocked_response = STUBBED_GOOGLE_BOOKS_RESPONSE.copy()
        mocked_response["items"][0]["volumeInfo"]["industryIdentifiers"][0][
            "identifier"
        ] = isbn

        return mocked_response
