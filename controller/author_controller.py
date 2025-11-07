class AuthorController:
    def __init__(self, auth_service, book_service, author_view):
        self.auth_service = auth_service
        self.book_service = book_service
        self.author_view = author_view

    def handle_publish_book(self):
        """Controller for publishing a book."""
        author = self.auth_service.get_current_user()
        if not author: return

        title, description, price, content_path = self.author_view.get_publish_book_details()
        try:
            book = self.book_service.publish_book(title, description, price, content_path, author)
            self.author_view.show_message(f"\nBook '{book.title}' has been published successfully!")
        except (ValueError, FileNotFoundError) as e:
            self.author_view.show_message(f"\nError: {e}")

    def handle_view_my_books(self):
        """Controller for an author to see their books."""
        author = self.auth_service.get_current_user()
        if not author: return
        
        books = self.book_service.get_author_books(author.id)
        self.author_view.display_author_books(books)

    def run_flow(self):
        """Manages the main menu loop for an author."""
        user = self.auth_service.get_current_user()
        while True:
            choice = self.author_view.show_author_menu(user)
            if choice == '1':
                self.handle_publish_book()
            elif choice == '2':
                self.handle_view_my_books()
            elif choice == '3':
                self.author_view.display_user_profile(user)
            elif choice == '4':
                self.auth_service.logout()
                self.author_view.show_message("\nYou have been logged out.")
                return
            else:
                self.author_view.show_message("Invalid choice. Please try again.")
