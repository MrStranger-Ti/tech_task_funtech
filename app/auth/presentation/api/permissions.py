from app.auth.presentation.api.dependancies import CurrentUserDep
from app.auth.presentation.exceptions import NotAuthorized
from app.users.domain.entities import UserEntity


def is_authenticated(user: CurrentUserDep) -> UserEntity:
    if not user:
        raise NotAuthorized

    return user
