from typing import Union

from dao.user_repository import UserRepository
from model.user import User, Role


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.current_user: Union[User, None] = None

    def get_current_user(self) -> Union[User, None]:
        """Returns the currently logged-in user."""
        return self.current_user

    def refresh_current_user(self):
        """Reloads the current user's data from the repository."""
        if self.current_user:
            self.current_user = self.user_repo.find_by_id(self.current_user.id)

    def register_user(self, name: str, email: str, password: str, role: Role) -> User:
        """
        Registers a new user.
        :param name: The name of the user.
        :param email: The email of the user.
        :param password: The user's password.
        :param role: The role of the user.
        :return: The newly created user.
        :raises ValueError: if a user with the same email already exists.
        """
        if self.user_repo.find_by_email(email):
            raise ValueError(f"User with email '{email}' already exists.")

        # New users get 100 credits by default
        initial_balance = 100.0
        
        # Storing password in plain text
        new_user = User(id=None, name=name, email=email, password=password, role=role, balance=initial_balance)
        
        return self.user_repo.add(new_user)

    def login_user(self, email: str, password: str) -> Union[User, None]:
        """
        Logs in a user.
        :param email: The user's email.
        :param password: The user's password.
        :return: The logged-in user, or None if login fails.
        """
        user = self.user_repo.find_by_email(email)
        if not user or user.is_banned:
            return None

        # Comparing plain text passwords
        if user.password == password:
            self.current_user = user
            return user
        
        return None

    def logout(self):
        """Logs out the current user."""
        self.current_user = None
