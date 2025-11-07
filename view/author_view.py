from typing import List
from view.main_view import print_header
from model.user import User
from model.book import Book

class AuthorView:
    def show_author_menu(self, user: User):
        print_header(f"Author Menu | Logged in as {user.name}")
        print("1. Publish a New Book")
        print("2. View My Published Books")
        print("3. View My Profile")
        print("4. Logout")
        return input("Choose an option: ")

    def get_publish_book_details(self):
        print_header("Publish New Book")
        title = input("Book Title: ")
        description = input("Book Description: ")
        while True:
            try:
                price = float(input("Price (credits): "))
                break
            except ValueError:
                self.show_message("Invalid price. Please enter a number.")
        
        content_path = input("Path to content file (e.g., 'books/my_book.txt'): ")
        return title, description, price, content_path

    def display_author_books(self, books: List[Book]):
        print_header("My Published Books")
        if not books:
            self.show_message("You haven't published any books yet.")
            return
        
        for book in books:
            avg_rating = f"{book.avg_rating():.1f}/5.0" if book.ratings else "No ratings"
            print(f"- '{book.title}' - Rating: {avg_rating} ({len(book.ratings)} ratings)")
        input("\nPress Enter to return to the menu...")

    def display_user_profile(self, user: User):
        """Displays the current user's profile."""
        print_header("My Profile")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role.capitalize()}")
        print(f"Balance: {user.balance} credits")
        input("\nPress Enter to return to the menu...")

    def show_message(self, message):
        print(f"\n{message}")
