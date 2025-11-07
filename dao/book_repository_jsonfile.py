from typing import List

from dao.book_repository import BookRepository
from dao.id_generator import IdGenerator
from dao.repository_jsonfile import RepositoryJsonFile
from decorators.singleton import singleton
from model.book import Book, Rating


@singleton
class BookRepositoryJsonFile(BookRepository, RepositoryJsonFile):
    def __init__(self, filename: str, id_generator: IdGenerator):
        # Note: We need to include Rating here so the deserializer knows about it
        super().__init__(filename, id_generator, {Book, Rating})

    def find_by_title(self, title: str) -> List[Book]:
        self.load_from_file()
        return [
            book for book in self.find_all()
            if title.lower() in book.title.lower()
        ]

    def find_by_author_id(self, author_id: str) -> List[Book]:
        self.load_from_file()
        return [
            book for book in self.find_all()
            if book.author_id == author_id
        ]
