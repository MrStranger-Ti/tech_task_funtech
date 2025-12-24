from sqlalchemy import insert, select, exists

from app.core.infrastructure.db.repositories import SQLAlchemyRepository
from app.users.domain.entities import UserEntity
from app.users.domain.interfaces.repositories import IUserRepository
from app.users.domain.specifications import UserCreateSpec
from app.users.infrastructure.db.models import UserModel


class UserRepository(IUserRepository, SQLAlchemyRepository):
    async def create(self, spec: UserCreateSpec) -> UserEntity:
        stmt = insert(UserModel).values(**spec.model_dump()).returning(UserModel)
        user = await self.session.scalar(stmt)
        return UserEntity.model_validate(user)

    async def email_exists(self, email: str) -> bool:
        stmt = select(exists().where(UserModel.email == email))
        return await self.session.scalar(stmt)

    async def get_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.email == email)
        user = await self.session.scalar(stmt)
        return UserEntity.model_validate(user) if user else None

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        user = await self.session.scalar(stmt)
        return UserEntity.model_validate(user) if user else None
