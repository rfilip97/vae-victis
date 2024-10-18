from utils.step import Step
from books.models import Book


class SaveBookToDb(Step):
    def perform(self, context):
        book_data = context.book_data

        Book.objects.create(
            isbn=book_data["isbn"],
            title=book_data["title"],
            author=book_data["author"],
            image_url=book_data["thumbnail"],
        )
