from utils.step import Step
from books.models import Book
from rest_framework import status


class GetLocalBook(Step):
    def perform(self, context):
        try:
            book = Book.objects.get(isbn=context.isbn)

            context.response_body = self._response(book)
            context.status_code = status.HTTP_200_OK
        except Book.DoesNotExist:
            pass

    def _response(self, book):
        return {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "thumbnail": book.image_url,
        }
