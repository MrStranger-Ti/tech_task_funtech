from app.core.application.use_cases import UseCase
from app.core.domain.interfaces.unit_of_work import IUnitOfWork
from app.users.application.dtos import UserCreateDTO
from app.users.application.exceptions import EmailAlreadyExists
from app.users.domain.entities import UserEntity
from app.users.domain.interfaces.repositories import IUserRepository
from app.users.domain.interfaces.services import IPasswordHasher
from app.users.domain.specifications import UserCreateSpec


class UserRegisterUC(UseCase):
    """
    Register a new user.

    Before creation check user in db by email.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self.uow: IUnitOfWork = uow
        self.user_repo: IUserRepository = user_repo
        self.password_hasher: IPasswordHasher = password_hasher

    async def execute(self, dto: UserCreateDTO) -> UserEntity:
        async with self.uow:
            if await self.user_repo.email_exists(email=dto.email):
                raise EmailAlreadyExists(f"Email {dto.email} already exists.")

            user = await self.user_repo.create(
                spec=UserCreateSpec(
                    email=dto.email,
                    password=self.password_hasher.hash(dto.password),
                ),
            )

            await self.uow.commit()

        return user
