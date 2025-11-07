class AdminController:
    def __init__(self, auth_service, admin_service, book_controller, admin_view):
        self.auth_service = auth_service
        self.admin_service = admin_service
        self.book_controller = book_controller
        self.admin_view = admin_view

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

    def run_flow(self):
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
                self.book_controller.handle_browse_books()
            elif choice == '5':
                self.auth_service.logout()
                self.admin_view.show_message("\nYou have been logged out.")
                return
            else:
                self.admin_view.show_message("Invalid choice. Please try again.")
