import enum
from datetime import datetime

from app.core.domain.entities import Entity


class StatusType(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


class OrderItemsEntity(Entity):
    name: str
    price: float


class OrderEntity(Entity):
    id: int
    items: list[OrderItemsEntity]
    total_price: float
    status: StatusType
    created_at: datetime
    user_id: int
