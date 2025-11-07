from typing import List, Dict
from model.book import Book
from model.user import User
from services.billing_service import BillingService

class BookView:
    def __init__(self, billing_service: BillingService):
        self.billing_service = billing_service

    def display_books_list(self, books: List[Book], authors: Dict[str, str]):
        """Displays a list of books."""
        print("\n--- Available Books ---")
        if not books:
            print("No books available at the moment.")
            return
        
        for i, book in enumerate(books):
            avg_rating, num_ratings = book.get_average_rating()
            rating_str = f"{avg_rating:.1f}/5.0" if num_ratings > 0 else "No ratings yet"
            print(f"{i + 1}. '{book.title}' by {authors.get(book.author_id, 'Unknown')} - Price: {book.price:.2f} credits - Rating: {rating_str}")

    def display_book_details(self, book: Book, author_name: str, is_purchased: bool, is_reader: bool):
        """Displays the full details of a single book and the available actions."""
        print(f"\n--- Book Details: {book.title.upper()} ---")
        print(f"Author: {author_name}")
        print(f"Description: {book.description}")
        print(f"Price: {book.price:.2f} credits")
        
        avg_rating, num_ratings = book.get_average_rating()
        rating_str = f"{avg_rating:.1f}/5.0 from {num_ratings} ratings" if num_ratings > 0 else "No ratings yet"
        print(f"Average Rating: {rating_str}.")
        print("--------------------")
        
        # Display available action text
        if is_reader:
            if is_purchased:
                print("Action: You already own this book. You can read it from 'My Purchased Books'.")
            else:
                print(f"Action: Purchase this book for {book.price:.2f} credits.")
        else:
            print("Action: Log in as a reader to purchase this book.")
        print("--------------------")

    def get_book_choice(self) -> str:
        """Asks the user to choose a book from the list."""
        return input("\nEnter book number to see details (or 'q' to return): ")

    def get_purchase_action(self) -> str:
        """Asks the user if they want to purchase the book."""
        return input("\nPress 'p' to purchase, or Enter to return... ")

    def get_return_action(self):
        """Asks the user to press Enter to return."""
        input("\nPress Enter to return... ")

    def show_message(self, message: str):
        print(message)
