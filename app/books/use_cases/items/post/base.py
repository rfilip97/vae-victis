from utils.use_case import UseCase
from utils.context import Context
from .prepare_params import PrepareParams
from .get_book_by_isbn import GetBookByIsbn
from .add_item_and_user_book import AddItemAndUserBook
from .prepare_response import PrepareResponse


class AddItem(UseCase):
    def perform(self, user, params):
        self.steps = [PrepareParams, GetBookByIsbn, AddItemAndUserBook, PrepareResponse]

        return super().perform(Context(user=user, params=params))
