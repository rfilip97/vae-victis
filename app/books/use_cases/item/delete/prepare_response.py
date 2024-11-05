from utils.step import Step
from rest_framework.response import Response
from rest_framework import status


class PrepareResponse(Step):
    def perform(self, context):
        context.message = "Item deleted successfully"
        context.status_code = status.HTTP_200_OK
