from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        item = context.item
        user_book = context.user_book

        return Response(
            self._item_data_from(item, user_book), status=status.HTTP_200_OK
        )

    def _item_data_from(self, item, user_book):
        return {
            "id": item.id,
            "isbn": user_book.book.isbn,
            "title": user_book.title_override or user_book.book.title,
            "author": user_book.author_override or user_book.book.author,
            "thumbnail": user_book.book.image_url,
            "quantity": user_book.quantity,
        }
