from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict

from app.core.domain.entities import Entity


class UserEntity(Entity):
    id: int | None = None
    email: str
    password: str
    is_active: bool = True
    created_at: datetime | None = None
    last_login: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
