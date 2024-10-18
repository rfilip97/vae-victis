from utils.step import Step
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        book_data = context.book_data

        context.response_body = book_data
        context.status_code = status.HTTP_200_OK
