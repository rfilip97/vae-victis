from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory


class ScanBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        isbn = request.GET.get("isbn", None)

        if isbn:
            return self.fetch_book_info_for(isbn)
        else:
            return Response({"error": "ISBN not provided"}, status=status.HTTP_400_BAD_REQUEST)

    def fetch_book_info_for(self, isbn):
        books_repository = BooksRepositoryFactory.get_repository()

        try:
            book_info = books_repository.get_book_info(isbn)
            return Response(book_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

