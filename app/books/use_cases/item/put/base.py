from utils.use_case import UseCase
from .validate_params import ValidateParams
from .get_item import GetItem
from .get_user_book import GetUserBook
from .update_user_book import UpdateUserBook
from .prepare_response import PrepareResponse


class UpdateItem(UseCase):
    def perform(self, user, item_id, params):
        self.steps = [
            ValidateParams,
            GetItem,
            GetUserBook,
            UpdateUserBook,
            PrepareResponse,
        ]

        return super().perform({"user": user, "item_id": item_id, "params": params})
