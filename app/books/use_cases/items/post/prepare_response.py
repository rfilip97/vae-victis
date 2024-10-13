from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        book = context["book"]

        return Response(
            {"message": f"Book '{book.title}' has been added to your items."},
            status=status.HTTP_201_CREATED,
        )
