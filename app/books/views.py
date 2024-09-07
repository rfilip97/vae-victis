from django.http import JsonResponse
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory


def scan_book(request):
    isbn = request.GET.get("isbn", None)

    if isbn:
        return fetch_book_info_for(isbn)
    else:
        return JsonResponse({"error": "ISBN not provided"}, status=400)


def fetch_book_info_for(isbn):
    books_repository = BooksRepositoryFactory.get_repository()

    try:
        book_info = books_repository.get_book_info(isbn)
        return JsonResponse(book_info, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
