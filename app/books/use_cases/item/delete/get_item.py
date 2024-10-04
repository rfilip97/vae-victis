from utils.step import Step
from books.models import Item
from rest_framework.response import Response
from rest_framework import status


class GetItem(Step):
    def perform(self, context):
        user = context["user"]
        item_id = context["item_id"]

        try:
            context["item"] = Item.objects.get(id=item_id, user=user)

        except Item.DoesNotExist:
            return Response(
                {"error": "Item not found or does not belong to you"},
                status=status.HTTP_404_NOT_FOUND,
            )
