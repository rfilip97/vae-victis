from rest_framework import status
from rest_framework.response import Response
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory
from books.models import Book


def get_local_book(isbn):
    try:
        book = Book.objects.get(isbn=isbn)

        return {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "thumbnail": book.image_url,
        }
    except Book.DoesNotExist:
        return None


def fetch_and_save_book(isbn):
    try:
        book_info = fetch_book(isbn)

        if book_info["totalItems"] == 0:
            return Response(
                {"error": "No book found with the provided ISBN"},
                status=status.HTTP_404_NOT_FOUND,
            )

        book_data = parse_book_data(book_info["items"][0]["volumeInfo"])

        save_book_to_db(book_data)

        return Response(book_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def fetch_book(isbn):
    return BooksRepositoryFactory.get_repository().get_book_info(isbn)


def save_book_to_db(book_data):
    Book.objects.create(
        isbn=book_data["isbn"],
        title=book_data["title"],
        author=book_data["author"],
        image_url=book_data["thumbnail"],
    )


def parse_book_data(book_data):
    return {
        "isbn": next(
            (
                identifier["identifier"]
                for identifier in book_data.get("industryIdentifiers", [])
                if identifier["type"] == "ISBN_13"
            ),
            "Not available",
        ),
        "title": book_data.get("title", "Title not available"),
        "author": ", ".join(book_data.get("authors", ["Author not available"])),
        "thumbnail": book_data.get("imageLinks", {}).get(
            "thumbnail", "Thumbnail not available"
        ),
    }


class ScanBook:
    @staticmethod
    def perform(isbn):
        if not isbn:
            return Response(
                {"error": "ISBN not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        local_book = get_local_book(isbn)

        if local_book:
            return Response(local_book, status=status.HTTP_200_OK)

        return fetch_and_save_book(isbn)
