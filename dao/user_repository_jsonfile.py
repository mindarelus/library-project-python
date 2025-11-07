from dao.id_generator import IdGenerator
from dao.repository_jsonfile import RepositoryJsonFile
from dao.user_repository import UserRepository
from decorators.singleton import singleton
from model.user import User


@singleton
class UserRepositoryJsonFile(UserRepository, RepositoryJsonFile):
    def __init__(self, filename: str, id_generator: IdGenerator):
        super().__init__(filename, id_generator, {User})

    def find_by_email(self, email: str):
        self.load_from_file()
        for entity in self.find_all():
            if entity.email == email:
                return entity
        return None
