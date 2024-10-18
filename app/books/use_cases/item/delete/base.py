from utils.use_case import UseCase
from utils.context import Context
from .get_item import GetItem
from .get_user_book import GetUserBook
from .delete_related_resources import DeleteRelatedResources
from .prepare_response import PrepareResponse


class DeleteItem(UseCase):
    def perform(self, user, item_id):
        self.steps = [GetItem, GetUserBook, DeleteRelatedResources, PrepareResponse]

        return super().perform(Context(user=user, item_id=item_id))
