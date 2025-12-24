from pydantic import EmailStr

from app.core.application.dtos import DTO


class TokenDataDTO(DTO):
    sub: str
    email: str
    iat: float
    exp: float
    token_type: str


class CredentialsDTO(DTO):
    email: EmailStr
    password: str


class TokenDTO(DTO):
    access: str
    type: str
