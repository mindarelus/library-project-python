import os
from typing import List, Union

from dao.book_repository import BookRepository
from dao.purchase_repository import PurchaseRepository
from dao.user_repository import UserRepository
from model.book import Book, Rating
from model.user import User


class BookService:
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository, purchase_repo: PurchaseRepository):
        self.book_repo = book_repo
        self.user_repo = user_repo
        self.purchase_repo = purchase_repo

    def publish_book(self, title: str, description: str, price: float, content_path: str, author: User) -> Book:
        """
        Publishes a new book for an author.
        :param title: The title of the book.
        :param description: A short description.
        :param price: The price of the book.
        :param content_path: The path to the .txt file with the content.
        :param author: The author (User object) publishing the book.
        :return: The newly published book.
        :raises ValueError: if the user is not an author or content file is not found.
        """
        if author.role != 'author':
            raise ValueError("Only authors can publish books.")
        
        if not os.path.exists(content_path):
            raise FileNotFoundError(f"Content file not found at: {content_path}")

        new_book = Book(id=None, title=title, description=description, price=price,
                        content_path=content_path, author_id=author.id)
        
        return self.book_repo.add(new_book)

    def get_all_books(self) -> List[Book]:
        """Returns a list of all books."""
        return self.book_repo.find_all()

    def get_book_by_id(self, book_id: str) -> Union[Book, None]:
        """Finds a book by its ID."""
        return self.book_repo.find_by_id(book_id)

    def read_book_content(self, book: Book) -> str:
        """
        Reads the content of a book from its file.
        :param book: The book to read.
        :return: The content of the book as a string.
        :raises FileNotFoundError: if the content file is missing.
        """
        if not os.path.exists(book.content_path):
            raise FileNotFoundError(f"Content file for '{book.title}' is missing!")
        
        with open(book.content_path, 'r', encoding='utf-8') as f:
            return f.read()

    def rate_book(self, book: Book, reader: User, value: int, comment: str = "") -> Book:
        """
        Allows a reader to rate a book they have purchased.
        :param book: The book to be rated.
        :param reader: The user rating the book.
        :param value: The rating value (1-5).
        :param comment: An optional comment.
        :return: The updated book.
        :raises ValueError: if the user is not a reader, the value is invalid, or the book is not purchased.
        """
        if reader.role != 'reader':
            raise ValueError("Only readers can rate books.")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        
        if not self.purchase_repo.find_by_reader_and_book(reader.id, book.id):
            raise ValueError("You can only rate books you have purchased.")

        # Check if this reader has already rated this book
        existing_rating = next((r for r in book.ratings if r.reader_id == reader.id), None)
        if existing_rating:
            # Update existing rating
            existing_rating.value = value
            existing_rating.comment = comment
        else:
            # Add new rating
            new_rating = Rating(reader_id=reader.id, value=value, comment=comment)
            book.ratings.append(new_rating)

        return self.book_repo.edit(book)

    def get_author_books(self, author_id: str) -> List[Book]:
        """Gets all books published by a specific author."""
        return self.book_repo.find_by_author_id(author_id)
