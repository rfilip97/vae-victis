from utils.step import Step


class DeleteRelatedResources(Step):
    def perform(self, context):
        context["user_book"].delete()
        context["item"].delete()
