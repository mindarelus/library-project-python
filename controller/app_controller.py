class AppController:
    def __init__(self, auth_service, book_service, billing_service, admin_service, config_service,
                 guest_view, reader_view, author_view, book_view, admin_view):
        self.auth_service = auth_service
        self.book_service = book_service
        self.billing_service = billing_service
        self.admin_service = admin_service
        self.config_service = config_service
        self.guest_view = guest_view
        self.reader_view = reader_view
        self.author_view = author_view
        self.book_view = book_view
        self.admin_view = admin_view

    # --- Guest Handlers ---
    def handle_register(self):
        """Controller for user registration."""
        try:
            name, email, password, role = self.guest_view.get_registration_details()
            user = self.auth_service.register_user(name, email, password, role)
            self.guest_view.show_message(f"\nRegistration successful! Welcome, {user.name}.\nAn initial balance of {user.balance} credits has been added.")
        except ValueError as e:
            self.guest_view.show_message(f"\nError: {e}")

    def handle_login(self):
        """Controller for user login."""
        email, password = self.guest_view.get_login_details()
        user = self.auth_service.login_user(email, password)
        if user:
            self.guest_view.show_message(f"\nWelcome back, {user.name}!")
        else:
            self.guest_view.show_message("\nInvalid email or password, or your account is banned.")

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

    # --- Reader Handlers ---
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

    # --- Author Handlers ---
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

    # --- Admin Handlers ---
    def handle_configure_book_sort(self):
        """Controller for configuring the global book sort order."""
        current_strategy = self.config_service.get_book_sort_strategy()
        choice = self.admin_view.show_book_sort_config_menu(current_strategy)

        if choice in ['publish_date', 'price']:
            self.config_service.set_book_sort_strategy(choice)
            self.admin_view.show_message(f"\nBook sort order has been updated to '{choice}'.")
        elif choice == 'cancel':
            self.admin_view.show_message("\nOperation cancelled.")
        else:
            self.admin_view.show_message("\nInvalid choice.")

    def handle_list_all_users(self):
        """Controller for listing all users for the admin."""
        admin = self.auth_service.get_current_user()
        if not admin: return
        
        users = self.admin_service.get_all_users_except(admin.id)
        self.admin_view.display_all_users(users)
        self.admin_view.get_return_action()

    def handle_toggle_ban_user(self):
        """Controller for banning or unbanning a user."""
        admin = self.auth_service.get_current_user()
        if not admin: return

        users = self.admin_service.get_all_users_except(admin.id)
        self.admin_view.display_all_users(users)
        if not users:
            return

        try:
            choice = self.admin_view.get_user_choice("Enter the number of the user to ban/unban (or 'q' to cancel): ")
            if choice.lower() == 'q': return

            user_index = int(choice) - 1
            if 0 <= user_index < len(users):
                user_to_toggle = users[user_index]
                if self.admin_view.get_ban_confirmation(user_to_toggle):
                    self.admin_service.toggle_ban_status(user_to_toggle)
                    action = "banned" if user_to_toggle.is_banned else "unbanned"
                    self.admin_view.show_message(f"\nUser '{user_to_toggle.name}' has been successfully {action}.")
                else:
                    self.admin_view.show_message("\nOperation cancelled.")
            else:
                self.admin_view.show_message("Invalid user number.")
        except ValueError:
            self.admin_view.show_message("Invalid input. Please enter a number.")

    def handle_add_credits_to_user(self):
        """Controller for adding credits to a user."""
        admin = self.auth_service.get_current_user()
        if not admin: return

        users = self.admin_service.get_all_users_except(admin.id)
        self.admin_view.display_all_users(users)
        if not users:
            return

        try:
            choice = self.admin_view.get_user_choice("Enter the number of the user to add credits to (or 'q' to cancel): ")
            if choice.lower() == 'q': return

            user_index = int(choice) - 1
            if 0 <= user_index < len(users):
                user_to_credit = users[user_index]
                amount = self.admin_view.get_credits_amount()
                if amount is not None:
                    self.admin_service.add_credits(user_to_credit, amount)
                    self.admin_view.show_message(f"\nSuccessfully added {amount:.2f} credits to '{user_to_credit.name}'.")
            else:
                self.admin_view.show_message("Invalid user number.")
        except ValueError:
            self.admin_view.show_message("Invalid input. Please enter a number.")

    # --- Main Menu Flows ---
    def run_guest_flow(self):
        """Manages the main menu loop for a guest user."""
        while True:
            choice = self.guest_view.show_guest_menu()
            if choice == '1':
                self.handle_login()
                if self.auth_service.get_current_user():
                    return
            elif choice == '2':
                self.handle_register()
            elif choice == '3':
                self.handle_browse_books()
            elif choice == '4':
                return "exit"
            else:
                self.guest_view.show_message("Invalid choice. Please try again.")

    def run_reader_flow(self):
        """Manages the main menu loop for a reader."""
        user = self.auth_service.get_current_user()
        while True:
            choice = self.reader_view.show_reader_menu(user)
            if choice == '1':
                self.handle_browse_books()
            elif choice == '2':
                self.handle_view_my_purchased_books()
            elif choice == '3':
                self.handle_rate_book()
            elif choice == '4':
                self.reader_view.display_user_profile(user)
            elif choice == '5':
                self.auth_service.logout()
                self.guest_view.show_message("\nYou have been logged out.")
                return
            else:
                self.reader_view.show_message("Invalid choice. Please try again.")

    def run_author_flow(self):
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
                self.guest_view.show_message("\nYou have been logged out.")
                return
            else:
                self.author_view.show_message("Invalid choice. Please try again.")

    def run_admin_flow(self):
        """Manages the main menu loop for an admin."""
        user = self.auth_service.get_current_user()
        while True:
            choice = self.admin_view.show_admin_menu(user)
            if choice == '1':
                self.handle_list_all_users()
            elif choice == '2':
                self.handle_toggle_ban_user()
            elif choice == '3':
                self.handle_add_credits_to_user()
            elif choice == '4':
                self.handle_browse_books()
            elif choice == '5':
                self.handle_configure_book_sort()
            elif choice == '6':
                self.auth_service.logout()
                self.guest_view.show_message("\nYou have been logged out.")
                return
            else:
                self.admin_view.show_message("Invalid choice. Please try again.")
