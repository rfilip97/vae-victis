from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory
from .models import Book


class ScanBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        isbn = request.GET.get("isbn", None)

        if not isbn:
            return Response(
                {"error": "ISBN not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        local_book = self.get_local_book(isbn)

        if local_book:
            return Response(local_book, status=status.HTTP_200_OK)

        return self.fetch_and_save_book(isbn)

    def get_local_book(self, isbn):
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

    def fetch_and_save_book(self, isbn):
        try:
            book_info = self.fetch_book(isbn)

            if book_info["totalItems"] == 0:
                return Response(
                    {"error": "No book found with the provided ISBN"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            book_data = self.parse_book_data(book_info["items"][0]["volumeInfo"])

            self.save_book_to_db(book_data)

            return Response(book_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def fetch_book(self, isbn):
        return BooksRepositoryFactory.get_repository().get_book_info(isbn)

    def save_book_to_db(self, book_data):
        Book.objects.create(
            isbn=book_data["isbn"],
            title=book_data["title"],
            author=book_data["author"],
            image_url=book_data["thumbnail"],
        )

    def parse_book_data(self, book_data):
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
