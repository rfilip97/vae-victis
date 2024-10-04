class UseCase:
    steps = []

    def perform(self, context):
        for step_class in self.steps:
            step = step_class()
            result = step.perform(context)

            if result is not None:
                return result
