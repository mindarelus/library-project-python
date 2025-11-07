class GuestController:
    def __init__(self, auth_service, book_controller):
        self.auth_service = auth_service
        self.book_controller = book_controller
        self.guest_view = auth_service.guest_view # Assuming guest_view is accessible

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

    def run_flow(self):
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
                self.book_controller.handle_browse_books()
            elif choice == '4':
                return "exit"
            else:
                self.guest_view.show_message("Invalid choice. Please try again.")
