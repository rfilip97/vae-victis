from utils.step import Step
from books.models import UserBook
from rest_framework import status


class GetUserBook(Step):
    def perform(self, context):
        user = context.user
        item = context.item

        resource = item.get_resource()

        try:
            context.user_book = UserBook.objects.get(user=user, book=resource)

        except UserBook.DoesNotExist:
            context.error = 'User-book association not found'
            context.status_code = status.HTTP_404_NOT_FOUND
