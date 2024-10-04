from utils.use_case import UseCase
from .prepare_params import PrepareParams
from .get_local_book import GetLocalBook
from .fetch_book import FetchBook
from .save_book_to_db import SaveBookToDb
from .prepare_response import PrepareResponse


class ScanBook(UseCase):
    def perform(self, isbn):
        self.steps = [
            PrepareParams,
            GetLocalBook,
            FetchBook,
            SaveBookToDb,
            PrepareResponse,
        ]

        return super().perform({"isbn": isbn})
