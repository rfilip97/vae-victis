from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from repositories.books_repository.book_repository_factory import BooksRepositoryFactory
from .models import Book, Item, UserBook
from .use_cases.item import DeleteItem, AddItem, GetItem


class ItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        return DeleteItem.perform(user=request.user, item_id=item_id)

    def put(self, request, item_id):
        return AddItem.perform(user=request.user, item_id=item_id, params=request.data)

    def get(self, request, item_id):
        return GetItem.perform(user=request.user, item_id=item_id)


class ItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        search_query = request.GET.get("search", None)

        return Response(
            self.get_items_for(request.user, search_query), status=status.HTTP_200_OK
        )

    def get_items_for(self, user, search_query=None):
        items = Item.objects.filter(user=user)
        items_data = []

        for item in items:
            resource = item.get_resource()

            try:
                user_book = UserBook.objects.get(user=user, book=resource)
                if self.is_match(resource, user_book, search_query):
                    items_data.append(self.item_data_from(item, resource, user_book))
            except UserBook.DoesNotExist:
                continue

        return items_data

    def is_match(self, resource, user_book, search_query):
        if not search_query:
            return True

        search_query = search_query.lower()

        return (
            search_query in (user_book.title_override or resource.title).lower()
            or search_query in (user_book.author_override or resource.author).lower()
        )

    def item_data_from(self, item, resource, user_book):
        return {
            "id": item.id,
            "isbn": resource.isbn,
            "title": user_book.title_override or resource.title,
            "author": user_book.author_override or resource.author,
            "thumbnail": resource.image_url,
            "quantity": user_book.quantity,
        }

    def post(self, request):
        item_type = request.data.get("type")
        isbn = request.data.get("isbn")
        title = request.data.get("title")
        author = request.data.get("author")

        if not self.is_supported_item_type(item_type):
            return Response(
                {"error": "Unsupported item type"}, status=status.HTTP_400_BAD_REQUEST
            )

        book = self.get_book_by_isbn(isbn)
        if book is None:
            return Response(
                {"error": "Book not found. Please scan the book first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if self.user_already_has_book(request.user, book):
            return Response(
                {"error": "This book has already been added to your items."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.add_item_and_user_book(request.user, book, item_type, title, author, isbn)

        return Response(
            {"message": f"Book '{book.title}' has been added to your items."},
            status=status.HTTP_201_CREATED,
        )

    def is_supported_item_type(self, item_type):
        return item_type == "book"

    def get_book_by_isbn(self, isbn):
        try:
            return Book.objects.get(isbn=isbn)
        except Book.DoesNotExist:
            return None

    def user_already_has_book(self, user, book):
        return UserBook.objects.filter(user=user, book=book).exists()

    def add_item_and_user_book(self, user, book, item_type, title, author, isbn):
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
