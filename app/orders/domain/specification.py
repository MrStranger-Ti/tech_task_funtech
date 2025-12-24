import re

from pydantic import Field, computed_field

from app.core.domain.specifications import Specification
from app.orders.domain.entities import StatusType, OrderItemsEntity


class OrderCreateSpec(Specification):
    items: list[OrderItemsEntity]
    status: StatusType = Field(default=StatusType.PENDING)
    user_id: int

    @computed_field
    @property
    def total_price(self) -> float:
        price = 0
        for item in self.items:
            price += item.price

        return price
