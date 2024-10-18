from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class ValidateParams(Step):
    def perform(self, context):
        params = context.params
        item_type = params.get("type")
        quantity = params.get("quantity")

        if not self._is_valid_item_type(item_type):
            return Response(
                {"error": "Unsupported item type"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not self._is_valid_quantity(quantity):
            return Response(
                {"error": "Quantity cannot be less than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _is_valid_item_type(self, item_type):
        return item_type == "book"

    def _is_valid_quantity(self, quantity):
        try:
            return int(quantity) >= 0
        except (ValueError, TypeError):
            return False
