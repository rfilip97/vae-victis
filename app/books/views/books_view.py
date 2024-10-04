from books.use_cases.books import ScanBook
from rest_framework import permissions
from rest_framework.views import APIView


class BooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return ScanBook().perform(request.GET.get("isbn", None))
