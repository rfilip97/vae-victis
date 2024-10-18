from utils.step import Step
from books.models import Book, UserBook
from rest_framework import status
from rest_framework.response import Response


class GetBookByIsbn(Step):
    def perform(self, context):
        isbn = context.isbn
        user = context.user
        book = None

        try:
            book = Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found. Please scan the book first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self._user_already_has_book(user, book):
            return Response(
                {"error": "This book has already been added to your items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        context.book = book

    def _user_already_has_book(self, user, book):
        return UserBook.objects.filter(user=user, book=book).exists()
