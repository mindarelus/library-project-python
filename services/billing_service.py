from typing import List
from dao.user_repository import UserRepository
from dao.book_repository import BookRepository
from dao.purchase_repository import PurchaseRepository
from model.user import User
from model.book import Book
from model.purchase import Purchase


class BillingService:
    def __init__(self, user_repo: UserRepository, book_repo: BookRepository, purchase_repo: PurchaseRepository):
        self.user_repo = user_repo
        self.book_repo = book_repo
        self.purchase_repo = purchase_repo

    def purchase_book(self, reader: User, book: Book) -> Purchase:
        """
        Handles the logic of a reader purchasing a book.
        :param reader: The user who is buying the book.
        :param book: The book being purchased.
        :return: The created Purchase object.
        :raises ValueError: if the purchase cannot be completed.
        """
        if reader.role != 'reader':
            raise ValueError("Only readers can purchase books.")

        if self.purchase_repo.find_by_reader_and_book(reader.id, book.id):
            raise ValueError("You have already purchased this book.")

        if reader.balance < book.price:
            raise ValueError(f"Insufficient funds. You need {book.price} credits, but you have {reader.balance}.")

        author = self.user_repo.find_by_id(book.author_id)
        if not author:
            # This should ideally not happen if data is consistent
            raise ValueError("Author of the book not found.")

        # Perform transaction
        reader.balance -= book.price
        author.balance += book.price

        # Update users in repository
        self.user_repo.edit(reader)
        self.user_repo.edit(author)

        # Create and save purchase record
        new_purchase = Purchase(id=None, book_id=book.id, reader_id=reader.id, price=book.price)
        return self.purchase_repo.add(new_purchase)

    def get_purchased_books_for_reader(self, reader_id: str) -> List[Book]:
        """
        Gets a list of all books purchased by a reader, sorted by purchase date (newest first).
        :param reader_id: The ID of the reader.
        :return: A list of Book objects.
        """
        purchases = self.purchase_repo.find_by_reader_id(reader_id)
        
        # Sort purchases by date, descending (newest first)
        purchases.sort(key=lambda p: p.purchase_date, reverse=True)

        # Fetch the book for each purchase
        purchased_books = []
        for p in purchases:
            book = self.book_repo.find_by_id(p.book_id)
            if book:
                purchased_books.append(book)
        return purchased_books

    def has_purchased_book(self, reader_id: str, book_id: str) -> bool:
        """
        Checks if a reader has purchased a specific book.
        """
        return self.purchase_repo.find_by_reader_and_book(reader_id, book_id) is not None
