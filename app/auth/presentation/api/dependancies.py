from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.application.use_cases import AuthenticationUC
from app.auth.domain.entities import AnonymousUserEntity
from app.auth.infrastructure.services.jwt import JWTAuthProvider
from app.users.domain.entities import UserEntity
from app.users.presentation.api.dependencies import UserRepoDep, PasswordHasherDep

security = HTTPBearer()


def get_auth_uc(
    user_repo: UserRepoDep,
    password_hasher: PasswordHasherDep,
) -> AuthenticationUC:
    return AuthenticationUC(
        user_repo=user_repo,
        token_provider=JWTAuthProvider(),
        password_hasher=password_hasher,
    )


AuthUCDep = Annotated[AuthenticationUC, Depends(get_auth_uc)]


async def get_current_user(
    user_repo: UserRepoDep,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserEntity | AnonymousUserEntity:
    auth_provider = JWTAuthProvider()
    token_data = auth_provider.read(credentials.credentials)
    if token_data is None:
        return AnonymousUserEntity()
    else:
        user = await user_repo.get_by_email(token_data.email)
        return user or AnonymousUserEntity()

    return await call_next(request)


CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]
