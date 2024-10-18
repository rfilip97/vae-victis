from utils.step import Step
from rest_framework import status
import pdb

class PrepareParams(Step):
    def perform(self, context):
        isbn = context.isbn

        if not isbn:
            pdb.set_trace()
            context.error = 'ISBN not provided'
            context.status_code = status.HTTP_404_NOT_FOUND
