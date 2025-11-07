from abc import abstractmethod

from dao.repository import Repository


class UserRepository(Repository):
    @abstractmethod
    def find_by_email(self, email: str):
        """
        Find user by email
        :param email: The email of the user
        :return: the user found or None
        """
        pass
