from sqlalchemy import insert, select, update

from app import OrderModel
from app.core.infrastructure.db.repositories import SQLAlchemyRepository
from app.orders.domain.entities import OrderEntity, StatusType
from app.orders.domain.interfaces.repositories import IOrderRepository
from app.orders.domain.specification import OrderCreateSpec


class OrderRepository(IOrderRepository, SQLAlchemyRepository):
    async def create(self, spec: OrderCreateSpec) -> OrderEntity:
        stmt = insert(OrderModel).values(spec.model_dump()).returning(OrderModel)
        order = await self.session.scalar(stmt)
        return OrderEntity.model_validate(order, from_attributes=True)

    async def get_by_id(self, order_id: int) -> OrderEntity | None:
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        order = await self.session.scalar(stmt)
        if order is not None:
            return OrderEntity.model_validate(order, from_attributes=True)

    async def update_status(self, order_id: int, status: StatusType) -> OrderEntity:
        stmt = (
            update(OrderModel)
            .where(OrderModel.id == order_id)
            .values(status=status)
            .returning(OrderModel)
        )
        order = await self.session.scalar(stmt)
        return OrderEntity.model_validate(order, from_attributes=True)

    async def get_user_orders(self, user_id: int) -> list[OrderEntity]:
        stmt = select(OrderModel).where(OrderModel.user_id == user_id)
        orders = await self.session.scalars(stmt)
        return [
            OrderEntity.model_validate(order, from_attributes=True) for order in orders
        ]
