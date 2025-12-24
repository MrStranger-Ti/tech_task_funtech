from app.auth.application.dtos import (
    CredentialsDTO,
)

from app.auth.domain.entities import TokenPairEntity
from app.auth.domain.interfaces.token_auth_provider import ITokenAuthProvider
from app.auth.domain.specifications import AuthTokenCreateSpec, CredentialsSpec
from app.core.application.use_cases import UseCase
from app.users.application.exceptions import InvalidCredentials
from app.users.domain.interfaces.repositories import IUserRepository
from app.users.domain.interfaces.services import IPasswordHasher


class AuthenticationUC(UseCase):
    """
    Check credentials and return access token.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        token_provider: ITokenAuthProvider,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.user_repo: IUserRepository = user_repo
        self.token_provider: ITokenAuthProvider = token_provider
        self.password_hasher: IPasswordHasher = password_hasher

    async def execute(self, dto: CredentialsDTO) -> TokenPairEntity:
        user = await self.user_repo.get_by_email(dto.email)
        if user is None or not self.password_hasher.check(dto.password, user.password):
            raise InvalidCredentials

        auth_token_spec = AuthTokenCreateSpec(sub=str(user.id), email=user.email)
        return TokenPairEntity(
            access=self.token_provider.create_access(auth_token_spec),
            type=self.token_provider.token_type,
        )
