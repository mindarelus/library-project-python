from typing import List, Union

from dao.id_generator import IdGenerator
from dao.repository_jsonfile import RepositoryJsonFile
from dao.purchase_repository import PurchaseRepository
from decorators.singleton import singleton
from model.purchase import Purchase


@singleton
class PurchaseRepositoryJsonFile(PurchaseRepository, RepositoryJsonFile):
    def __init__(self, filename: str, id_generator: IdGenerator):
        super().__init__(filename, id_generator, {Purchase})

    def find_by_reader_id(self, reader_id: str) -> List[Purchase]:
        self.load_from_file()
        return [
            purchase for purchase in self.find_all()
            if purchase.reader_id == reader_id
        ]

    def find_by_reader_and_book(self, reader_id: str, book_id: str) -> Union[Purchase, None]:
        self.load_from_file()
        for purchase in self.find_all():
            if purchase.reader_id == reader_id and purchase.book_id == book_id:
                return purchase
        return None
