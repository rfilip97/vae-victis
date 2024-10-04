from books.models import Book, Item, UserBook
from rest_framework import status
from rest_framework.response import Response


def is_supported_item_type(item_type):
    return item_type == "book"


def get_book_by_isbn(isbn):
    try:
        return Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return None


def user_already_has_book(user, book):
    return UserBook.objects.filter(user=user, book=book).exists()


def add_item_and_user_book(user, book, item_type, title, author, isbn):
    Item.objects.create(
        user=user,
        resource_type=item_type,
        resource_id=book.id,
    )

    UserBook.objects.create(
        user=user,
        book=book,
        title_override=title,
        author_override=author,
        isbn_override=isbn,
    )


class AddItem:
    @staticmethod
    def perform(user, params):
        item_type = params.get("type")
        isbn = params.get("isbn")
        title = params.get("title")
        author = params.get("author")

        if not is_supported_item_type(item_type):
            return Response(
                {"error": "Unsupported item type"}, status=status.HTTP_400_BAD_REQUEST
            )

        book = get_book_by_isbn(isbn)
        if book is None:
            return Response(
                {"error": "Book not found. Please scan the book first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user_already_has_book(user, book):
            return Response(
                {"error": "This book has already been added to your items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        add_item_and_user_book(user, book, item_type, title, author, isbn)

        return Response(
            {"message": f"Book '{book.title}' has been added to your items."},
            status=status.HTTP_201_CREATED,
        )
