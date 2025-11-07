from typing import List
from dao.user_repository import UserRepository
from model.user import User


class AdminService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_all_users_except(self, admin_id: str) -> List[User]:
        """Returns a list of all users, excluding the specified admin."""
        all_users = self.user_repo.find_all()
        return [user for user in all_users if user.id != admin_id]

    def toggle_ban_status(self, user: User) -> User:
        """Toggles the 'is_banned' status of a user."""
        user.is_banned = not user.is_banned
        return self.user_repo.edit(user)

    def add_credits(self, user: User, amount: float) -> User:
        """Adds a specified amount of credits to a user's balance."""
        if amount <= 0:
            raise ValueError("Credit amount must be positive.")
        user.balance += amount
        return self.user_repo.edit(user)
