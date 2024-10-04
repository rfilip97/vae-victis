from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareParams(Step):
    def perform(self, context):
        isbn = context.get("isbn", None)

        if not isbn:
            return Response(
                {"error": "ISBN not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
