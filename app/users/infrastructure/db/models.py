from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import String, text, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.infrastructure.db.database import BaseModel

if TYPE_CHECKING:
    from app.orders.infrastructure.db.models import OrderModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    password: Mapped[str] = mapped_column(String(length=255))
    is_active: Mapped[bool] = mapped_column(
        default=False,
        server_default=text("false"),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
    last_login: Mapped[datetime | None] = mapped_column()

    orders: Mapped[list[OrderModel]] = relationship(back_populates="user")
