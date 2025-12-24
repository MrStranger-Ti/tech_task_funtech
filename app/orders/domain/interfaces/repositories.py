import abc

from app.orders.domain.entities import OrderEntity, StatusType
from app.orders.domain.specification import OrderCreateSpec


class IOrderRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, spec: OrderCreateSpec) -> OrderEntity:
        pass

    @abc.abstractmethod
    async def get_by_id(self, order_id: int) -> OrderEntity | None:
        pass

    @abc.abstractmethod
    async def update_status(self, order_id: int, status: StatusType) -> OrderEntity:
        pass

    @abc.abstractmethod
    async def get_user_orders(self, user_id: int) -> list[OrderEntity]:
        pass
