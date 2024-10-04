from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
        )
