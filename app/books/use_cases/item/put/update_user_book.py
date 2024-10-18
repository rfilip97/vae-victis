from utils.step import Step


class UpdateUserBook(Step):
    def perform(self, context):
        user_book = context.user_book
        data = context.params

        user_book.title_override = data.get("title", user_book.title_override)
        user_book.author_override = data.get("author", user_book.author_override)
        user_book.isbn_override = data.get("isbn", user_book.isbn_override)
        user_book.quantity = data.get("quantity", user_book.quantity)

        user_book.save()
