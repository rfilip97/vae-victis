from utils.step import Step
from rest_framework import status


BOOK_TYPE = "book"


class PrepareParams(Step):
    def perform(self, context):
        params = context.params

        context.isbn = params.get("isbn")
        context.item_type = params.get("type")

        if not context.item_type == BOOK_TYPE:
            context.error = 'Unsupported item type'
            context.status_code = status.HTTP_400_BAD_REQUEST
