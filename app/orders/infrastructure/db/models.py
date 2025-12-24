from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Enum, func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.infrastructure.db.database import BaseModel
from app.orders.domain.entities import StatusType

if TYPE_CHECKING:
    from app import UserModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    items: Mapped[list] = mapped_column(JSON)
    total_price: Mapped[float]
    status: Mapped[StatusType] = mapped_column(Enum(StatusType))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    user: Mapped[UserModel] = relationship(back_populates="orders")
