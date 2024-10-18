from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        book_data = context.book_data

        return Response(book_data, status=status.HTTP_200_OK)
