import asyncio

from app.core.infrastructure.broker.taskiq import broker
from app.orders.domain.entities import OrderEntity


@broker.task("new_order")
async def create_order_task(order: OrderEntity) -> None:
    await asyncio.sleep(2)
    print(f"Order {order.id} processed")
