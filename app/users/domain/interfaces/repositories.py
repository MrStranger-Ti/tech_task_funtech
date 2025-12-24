import abc

from app.users.domain.entities import UserEntity
from app.users.domain.specifications import UserCreateSpec


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, spec: UserCreateSpec) -> UserEntity:
        pass

    @abc.abstractmethod
    async def email_exists(self, email: str) -> bool:
        pass

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        pass

    @abc.abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None:
        pass
