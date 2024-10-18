from utils.step import Step
from books.models import Book, UserBook
from rest_framework import status


class GetBookByIsbn(Step):
    def perform(self, context):
        isbn = context.isbn
        user = context.user
        book = None

        try:
            book = Book.objects.get(isbn=isbn)

            if self._user_already_has_book(user, book):
                context.error = 'This book has already been added to your items.'
                context.status_code = status.HTTP_400_BAD_REQUEST

            context.book = book

        except Book.DoesNotExist:
            context.error = 'Book not found. Please scan the book first.'
            context.status_code = status.HTTP_400_BAD_REQUEST

    def _user_already_has_book(self, user, book):
        return UserBook.objects.filter(user=user, book=book).exists()
