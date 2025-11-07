from abc import abstractmethod
from typing import List

from dao.repository import Repository
from model.book import Book


class BookRepository(Repository):
    @abstractmethod
    def find_by_title(self, title: str) -> List[Book]:
        """
        Find books by title (can be partial match)
        :param title: The title to search for
        :return: a list of books found
        """
        pass

    @abstractmethod
    def find_by_author_id(self, author_id: str) -> List[Book]:
        """
        Find all books by a given author
        :param author_id: The ID of the author
        :return: a list of books by that author
        """
        pass
