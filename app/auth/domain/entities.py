import enum

from app.core.domain.entities import Entity


class TokenType(enum.Enum):
    ACCESS = "access"


class TokenPairEntity(Entity):
    access: str
    type: str


class TokenDataEntity(Entity):
    sub: str
    email: str
    iat: float
    exp: float
    token_type: TokenType


class AnonymousUserEntity(Entity):
    id: None = None
    email: None = None
    password: None = None
    is_active: bool = False
    created_at: None = None
    last_login: None = None

    def __bool__(self) -> bool:
        return False
