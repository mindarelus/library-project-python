from abc import abstractmethod
from typing import List, Union

from dao.repository import Repository
from model.purchase import Purchase


class PurchaseRepository(Repository):
    @abstractmethod
    def find_by_reader_id(self, reader_id: str) -> List[Purchase]:
        """
        Finds all purchases made by a specific reader.
        :param reader_id: The ID of the reader.
        :return: A list of purchases.
        """
        pass

    @abstractmethod
    def find_by_reader_and_book(self, reader_id: str, book_id: str) -> Union[Purchase, None]:
        """
        Checks if a specific reader has purchased a specific book.
        :param reader_id: The ID of the reader.
        :param book_id: The ID of the book.
        :return: The Purchase object if found, otherwise None.
        """
        pass
