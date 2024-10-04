from utils.step import Step
from books.models import Book
from rest_framework.response import Response
from rest_framework import status


class GetLocalBook(Step):
    def perform(self, context):
        try:
            book = Book.objects.get(isbn=context["isbn"])

            return Response(self._response(book), status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            pass

    def _response(self, book):
        return {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "thumbnail": book.image_url,
        }
