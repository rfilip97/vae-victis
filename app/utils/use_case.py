from rest_framework.response import Response
from rest_framework import status


class UseCase:
    steps = []

    def perform(self, context):
        response = self._iterate_through_steps(context)

        return response if response is not None else self._default_response()

    def _iterate_through_steps(self, context):
        for step_class in self.steps:
            step = step_class()
            result = step.perform(context)

            if result is not None:
                return result

    def _default_response(self):
        return Response(status=status.HTTP_200_OK)
