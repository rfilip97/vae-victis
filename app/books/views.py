from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory


class ScanBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        isbn = request.GET.get("isbn", None)

        if isbn:
            return fetch_book_info_for(isbn)
        else:
            return Response(
                {"error": "ISBN not provided"}, status=status.HTTP_400_BAD_REQUEST
            )


def fetch_book_info_for(isbn):
    books_repository = BooksRepositoryFactory.get_repository()

    try:
        book_info = books_repository.get_book_info(isbn)

        if book_info["totalItems"] == 0:
            return Response(
                {"error": "No book found with the provided ISBN"},
                status=status.HTTP_404_NOT_FOUND,
            )

        book_data = book_info["items"][0]["volumeInfo"]

        return Response(parse_book_data(book_data), status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
