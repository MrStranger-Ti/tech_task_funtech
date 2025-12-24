import abc

from app.auth.domain.entities import TokenDataEntity
from app.auth.domain.specifications import AuthTokenCreateSpec


class ITokenAuthProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def token_type(self) -> str:
        pass

    @abc.abstractmethod
    def create_access(self, token_data: AuthTokenCreateSpec) -> str:
        pass

    @abc.abstractmethod
    def read(self, token: str) -> TokenDataEntity | None:
        pass
