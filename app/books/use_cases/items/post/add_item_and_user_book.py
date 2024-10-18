from utils.step import Step
from books.models import Item, UserBook


class AddItemAndUserBook(Step):
    def perform(self, context):
        user = context.user
        book = context.book
        item_type = context.item_type
        isbn = context.isbn
        title = book.title
        author = book.author

        self._create_item(user, item_type, book.id)
        self._create_user_book(user, book, title, author, isbn)

    def _create_item(self, user, item_type, book_id):
        Item.objects.create(
            user=user,
            resource_type=item_type,
            resource_id=book_id,
        )

    def _create_user_book(self, user, book, title, author, isbn):
        UserBook.objects.create(
            user=user,
            book=book,
            title_override=title,
            author_override=author,
            isbn_override=isbn,
        )
