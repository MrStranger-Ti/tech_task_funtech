from typing import Annotated

from fastapi import Depends

from app.core.presentation.api.dependencies import DBSessionDep, UOWDep
from app.users.application.use_cases import (
    UserRegisterUC,
)
from app.users.domain.interfaces.repositories import IUserRepository
from app.users.domain.interfaces.services import IPasswordHasher
from app.users.infrastructure.db.repositories import UserRepository
from app.users.infrastructure.services.password import BcryptPasswordHasher


def get_user_repository(session: DBSessionDep) -> IUserRepository:
    return UserRepository(session=session)


UserRepoDep = Annotated[IUserRepository, Depends(get_user_repository)]


def get_password_hasher() -> IPasswordHasher:
    return BcryptPasswordHasher()


PasswordHasherDep = Annotated[IPasswordHasher, Depends(get_password_hasher)]


def get_register_uc(
    uow: UOWDep,
    user_repo: UserRepoDep,
    password_hasher: PasswordHasherDep,
) -> UserRegisterUC:
    return UserRegisterUC(
        uow=uow,
        user_repo=user_repo,
        password_hasher=password_hasher,
    )


RegisterUCDep = Annotated[UserRegisterUC, Depends(get_register_uc)]
