from datetime import datetime

from pydantic import EmailStr

from app.core.application.dtos import DTO


class UserReadDTO(DTO):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    last_login: datetime | None = None


class UserCreateDTO(DTO):
    email: EmailStr
    password: str
