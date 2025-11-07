class ReaderController:
    def __init__(self, auth_service, book_service, billing_service, book_controller, reader_view):
        self.auth_service = auth_service
        self.book_service = book_service
        self.billing_service = billing_service
        self.book_controller = book_controller
        self.reader_view = reader_view

    def handle_rate_book(self):
        """Controller for rating a book."""
        reader = self.auth_service.get_current_user()
        if not reader: return

        authors = {user.id: user.name for user in self.auth_service.user_repo.find_all()}
        purchased_books = self.billing_service.get_purchased_books_for_reader(reader.id)
        self.reader_view.display_books_for_rating(purchased_books, authors, reader.id)

        if not purchased_books:
            return

        book_choice, value, comment = self.reader_view.get_rating_details()
        if not book_choice:
            return

        try:
            book_index = int(book_choice) - 1
            if 0 <= book_index < len(purchased_books):
                selected_book = purchased_books[book_index]
                self.book_service.rate_book(selected_book, reader, value, comment)
                self.reader_view.show_message("\nThank you for your feedback!")
            else:
                self.reader_view.show_message("Invalid book number.")
        except ValueError:
            self.reader_view.show_message("Please enter a valid number.")
        except Exception as e:
            self.reader_view.show_message(f"\nAn unexpected error occurred: {e}")

    def handle_view_my_purchased_books(self):
        """Controller for viewing and reading purchased books."""
        reader = self.auth_service.get_current_user()
        if not reader: return

        authors = {user.id: user.name for user in self.auth_service.user_repo.find_all()}

        while True:
            books = self.billing_service.get_purchased_books_for_reader(reader.id)
            self.reader_view.display_purchased_books(books, authors)
            
            choice = self.reader_view.get_book_to_read_choice()
            if choice.lower() == 'q':
                break
            
            try:
                book_index = int(choice) - 1
                if 0 <= book_index < len(books):
                    selected_book = books[book_index]
                    content = self.book_service.read_book_content(selected_book)
                    self.reader_view.display_book_content(selected_book.title, content)
                else:
                    self.reader_view.show_message("Invalid book number.")
            except (ValueError, FileNotFoundError) as e:
                self.reader_view.show_message(f"Error: {e}")

    def run_flow(self):
        """Manages the main menu loop for a reader."""
        user = self.auth_service.get_current_user()
        while True:
            choice = self.reader_view.show_reader_menu(user)
            if choice == '1':
                self.book_controller.handle_browse_books()
            elif choice == '2':
                self.handle_view_my_purchased_books()
            elif choice == '3':
                self.handle_rate_book()
            elif choice == '4':
                self.reader_view.display_user_profile(user)
            elif choice == '5':
                self.auth_service.logout()
                self.reader_view.show_message("\nYou have been logged out.")
                return
            else:
                self.reader_view.show_message("Invalid choice. Please try again.")
