from model.user import User
from typing import List, Dict
from model.book import Book


class ReaderView:
    def show_reader_menu(self, user: User) -> str:
        print(f"\n--- Reader Menu (Logged in as {user.name}, Balance: {user.balance:.2f}) ---")
        print("1. Browse All Books")
        print("2. My Purchased Books")
        print("3. Rate a Book")
        print("4. View My Profile")
        print("5. Logout")
        return input("Enter your choice: ")

    def get_rating_details(self) -> (str, int, str):
        print("\n--- Rate a Book ---")
        book_choice = input("Enter the number of the book you want to rate (or 'q' to cancel): ")
        if book_choice.lower() == 'q' or not book_choice:
            return None, None, None

        while True:
            try:
                value = int(input("Enter your rating (1-5): "))
                if 1 <= value <= 5:
                    break
                else:
                    print("Invalid rating. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        comment = input("Enter your comment (optional): ")
        return book_choice, value, comment

    def display_user_profile(self, user: User):
        print("\n--- Your Profile ---")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role.capitalize()}")
        print(f"Balance: {user.balance:.2f} credits")
        print("--------------------")

    def display_books_for_rating(self, books: List[Book], authors: Dict[str, str], reader_id: str):
        # The header is now printed in get_rating_details
        print("You can rate the following books you've purchased:")
        if not books:
            print("You have no purchased books to rate yet.")
            return
        
        for i, book in enumerate(books):
            # Find the user's existing rating for this book, if any
            user_rating = next((r for r in book.ratings if r.reader_id == reader_id), None)
            rating_str = f"Your rating: {user_rating.value}/5" if user_rating else "Not rated by you yet"
            author_name = authors.get(book.author_id, "Unknown")
            print(f" {i + 1}. {author_name} - {book.title} | {rating_str}")
        print("----------------------------------------------------")

    def display_purchased_books(self, books: List[Book], authors: Dict[str, str]):
        print("\n--- My Purchased Books (sorted by newest first) ---")
        if not books:
            print("You haven't purchased any books yet.")
            return
        
        for i, book in enumerate(books):
            author_name = authors.get(book.author_id, "Unknown Author")
            print(f"{i + 1}. {author_name} - {book.title}")
        print("----------------------------------------------------")

    def get_book_to_read_choice(self) -> str:
        return input("Enter the number of the book to read, or 'q' to return to the menu: ")

    def display_book_content(self, book_title: str, content: str):
        print(f"\n--- Reading: {book_title} ---")
        print(content)
        print("--- End of Book ---")
        input("\nPress Enter to continue...")

    def show_message(self, message: str):
        print(message)
