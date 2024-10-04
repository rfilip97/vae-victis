from utils.step import Step
from books.models import UserBook
from rest_framework.response import Response
from rest_framework import status


class GetUserBook(Step):
    def perform(self, context):
        user = context["user"]
        item = context["item"]

        resource = item.get_resource()

        try:
            context["user_book"] = UserBook.objects.get(user=user, book=resource)

        except UserBook.DoesNotExist:
            return Response(
                {"error": "User-book association not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
