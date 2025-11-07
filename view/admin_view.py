from typing import List, Union
from model.user import User
from services.config_service import SortOption


class AdminView:
    def show_admin_menu(self, admin: User) -> str:
        print(f"\n--- Admin Menu (Logged in as {admin.name}) ---")
        print("1. List All Users")
        print("2. Ban/Unban a User")
        print("3. Add Credits to User")
        print("4. Browse All Books")
        print("5. Configure Book Sort Order")
        print("6. Logout")
        return input("Enter your choice: ")

    def display_all_users(self, users: List[User]):
        print("\n--- All Registered Users ---")
        if not users:
            print("No other users found in the system.")
            return

        print(f"{'No.':<4} {'ID':<37} {'Name':<15} {'Email':<25} {'Role':<8} {'Balance':>10} {'Status':<10}")
        print("-" * 115)
        for i, user in enumerate(users):
            status = "Banned" if user.is_banned else "Active"
            print(f"{i + 1:<4} {user.id:<37} {user.name:<15} {user.email:<25} {user.role:<8} {user.balance:>10.2f} {status:<10}")
        print("-" * 115)

    def show_book_sort_config_menu(self, current_sort_strategy: SortOption) -> str:
        print("\n--- Configure Book Sort Order ---")
        print(f"Current sort order is by: '{current_sort_strategy}'")
        print("Choose a new sort order:")
        print("1. By Publication Date (newest first)")
        print("2. By Price (lowest first)")
        choice = input("Enter your choice (or 'q' to cancel): ")
        if choice == '1':
            return 'publish_date'
        elif choice == '2':
            return 'price'
        elif choice.lower() == 'q':
            return 'cancel'
        else:
            return 'invalid'

    def get_user_choice(self, prompt: str) -> str:
        return input(prompt)

    def get_credits_amount(self) -> Union[float, None]:
        try:
            amount = float(input("Enter the amount of credits to add: "))
            if amount <= 0:
                print("Amount must be a positive number.")
                return None
            return amount
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

    def get_return_action(self):
        """Asks the user to press Enter to return."""
        input("\nPress Enter to return... ")

    def get_ban_confirmation(self, user: User) -> bool:
        action = "UNBAN" if user.is_banned else "BAN"
        confirm = input(f"\nAre you sure you want to {action} the user '{user.name}'? (y/n): ")
        return confirm.lower() == 'y'

    def show_message(self, message: str):
        print(message)
