from utils.step import Step
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        book = context.book

        context.message = f"Book '{book.title}' has been added to your items."
        context.status_code = status.HTTP_201_CREATED
