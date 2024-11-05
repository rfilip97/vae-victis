from utils.step import Step
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory
from rest_framework import status


class FetchBook(Step):
    def perform(self, context):
        isbn = context.isbn

        book_info = BooksRepositoryFactory.get_repository().get_book_info(isbn)

        if book_info["totalItems"] == 0:
            context.error = "No book found with the provided ISBN"
            context.status_code = status.HTTP_404_NOT_FOUND

        context.book_data = self._parse_book_data(book_info)

    def _parse_book_data(self, book_data):
        book_info = book_data["items"][0]["volumeInfo"]

        return {
            "isbn": next(
                (
                    identifier["identifier"]
                    for identifier in book_info.get("industryIdentifiers", [])
                    if identifier["type"] == "ISBN_13"
                ),
                "Not available",
            ),
            "title": book_info.get("title", "Title not available"),
            "author": ", ".join(book_info.get("authors", ["Author not available"])),
            "thumbnail": book_info.get("imageLinks", {}).get(
                "thumbnail", "Thumbnail not available"
            ),
        }
