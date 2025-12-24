from pydantic import EmailStr

from app.core.domain.specifications import Specification


class AuthTokenCreateSpec(Specification):
    sub: str
    email: str


class CredentialsSpec(Specification):
    email: EmailStr
    password: str
