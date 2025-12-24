from datetime import datetime

from app.core.application.dtos import DTO
from app.orders.domain.entities import StatusType


class OrderItemsDTO(DTO):
    name: str
    price: float


class OrderReadDTO(DTO):
    id: int
    items: list[OrderItemsDTO]
    total_price: float
    status: StatusType
    created_at: datetime


class OrderCreateDTO(DTO):
    items: list[OrderItemsDTO]


class OrderUpdateDTO(DTO):
    status: StatusType
