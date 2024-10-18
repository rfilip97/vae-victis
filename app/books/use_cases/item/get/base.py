from utils.use_case import UseCase
from utils.context import Context
from .get_item import GetItem as GetBookItem
from .get_user_book import GetUserBook
from .prepare_response import PrepareResponse


class GetItem(UseCase):
    def perform(self, user, item_id):
        self.steps = [GetBookItem, GetUserBook, PrepareResponse]

        return super().perform(Context(user=user, item_id=item_id))
