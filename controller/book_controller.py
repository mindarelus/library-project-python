class BookController:
    def __init__(self, auth_service, book_service, billing_service, book_view):
        self.auth_service = auth_service
        self.book_service = book_service
        self.billing_service = billing_service
        self.book_view = book_view

    def handle_browse_books(self):
        """Controller for browsing all books."""
        books = self.book_service.get_all_books()
        authors = {user.id: user.name for user in self.auth_service.user_repo.find_all()}
        
        current_user = self.auth_service.get_current_user()
        is_reader = current_user and current_user.role == 'reader'

        self.book_view.display_books_list(books, authors)

        while True:
            choice = self.book_view.get_book_choice()
            if choice.lower() == 'q':
                break
            try:
                book_index = int(choice) - 1
                if 0 <= book_index < len(books):
                    selected_book = books[book_index]
                    author_name = authors.get(selected_book.author_id, "Unknown")
                    
                    is_purchased = False
                    if is_reader:
                        is_purchased = self.billing_service.has_purchased_book(current_user.id, selected_book.id)
                    
                    self.book_view.display_book_details(selected_book, author_name, is_purchased, is_reader)

                    if is_reader and not is_purchased:
                        action = self.book_view.get_purchase_action()
                        if action.lower() == 'p':
                            try:
                                self.billing_service.purchase_book(current_user, selected_book)
                                self.book_view.show_message(f"\nSuccessfully purchased '{selected_book.title}'.")
                                self.auth_service.refresh_current_user()
                            except ValueError as e:
                                self.book_view.show_message(f"\nPurchase failed: {e}")
                    else:
                        self.book_view.get_return_action()
                else:
                    self.book_view.show_message("Invalid book number.")
            except ValueError:
                self.book_view.show_message("Please enter a valid number.")
