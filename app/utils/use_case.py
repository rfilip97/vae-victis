from rest_framework.response import Response
from rest_framework import status


class UseCase:
    steps = []

    def perform(self, context):
        for step_class in self.steps:
            step = step_class()
            step.perform(context)

            if context.status_code is not None:
                if context.response_body is not None:
                    return Response(context.response_body, status=context.status_code)

                response_data = {}

                if context.message is not None:
                    response_data['message'] = context.message

                if context.error is not None:
                    response_data['error'] = context.error

                if context.errors is not None:
                    response_data['errors'] = context.errors

                return Response(response_data, status=context.status_code)

        return self._default_response()

    def _default_response(self):
        return Response(status=status.HTTP_200_OK)
