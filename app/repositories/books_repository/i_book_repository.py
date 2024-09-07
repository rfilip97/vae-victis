from abc import ABC, abstractmethod


class IBooksRepository(ABC):
    @abstractmethod
    def get_book_info(self, isbn):
        pass
