from app.core.application.use_cases import UseCase
from app.core.domain.interfaces.cache import ICacheClient
from app.core.domain.interfaces.unit_of_work import IUnitOfWork
from app.core.application.exceptions import NotFound
from app.orders.application.dtos import OrderCreateDTO, OrderUpdateDTO
from app.orders.domain.entities import OrderEntity, StatusType
from app.orders.domain.interfaces.repositories import IOrderRepository
from app.orders.domain.specification import OrderCreateSpec
from app.orders.infrastructure.broker.tasks import create_order_task
from app.users.domain.interfaces.repositories import IUserRepository


class OrderCreateUC(UseCase):
    """
    Create a new order and task "new_order" for broker.
    """

    def __init__(self, uow: IUnitOfWork, order_repo: IOrderRepository) -> None:
        self.uow = uow
        self.order_repo = order_repo

    async def execute(self, dto: OrderCreateDTO, user_id: int) -> OrderEntity:
        async with self.uow:
            order = await self.order_repo.create(
                spec=OrderCreateSpec(
                    items=dto.model_dump().get("items"),
                    user_id=user_id,
                ),
            )

            await self.uow.commit()

        await create_order_task.kiq(order)

        return order


class OrderGetUC(UseCase):
    """
    Getting order by id from db with cache.
    """

    def __init__(
        self,
        cache_client: ICacheClient,
        order_repo: IOrderRepository,
        cache_ttl: int = 60 * 5,
    ) -> None:
        self.cache_client = cache_client
        self.order_repo = order_repo
        self.cache_ttl = cache_ttl

    async def execute(self, order_id: int) -> OrderEntity:
        cache_key = f"orders:{order_id}"

        order = await self.cache_client.get(key=cache_key)
        if order is not None:
            return OrderEntity.model_validate_json(order)

        order = await self.order_repo.get_by_id(order_id)
        if order is not None:
            await self.cache_client.set(
                cache_key,
                order.model_dump_json(),
                time=self.cache_ttl,
            )
            return order

        raise NotFound(detail=f"Order {order_id} not found")


class OrderUpdateUC(UseCase):
    """
    Updating order and refresh cache.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        cache_client: ICacheClient,
        order_repo: IOrderRepository,
        cache_ttl: int = 60 * 5,
    ) -> None:
        self.uow = uow
        self.cache_client = cache_client
        self.order_repo = order_repo
        self.cache_ttl = cache_ttl

    async def execute(self, order_id: int, dto: OrderUpdateDTO) -> OrderEntity:
        async with self.uow:
            cache_key = f"orders:{order_id}"

            order = await self.order_repo.get_by_id(order_id)
            if order is None:
                raise NotFound(detail=f"Order {order_id} not found")

            order = await self.order_repo.update_status(order_id, dto.status)

            await self.cache_client.set(
                cache_key,
                order.model_dump_json(),
                time=self.cache_ttl,
            )

            await self.uow.commit()

        return order


class UserOrdersUC(UseCase):
    """
    Getting user's orders.'
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        order_repo: IOrderRepository,
    ) -> None:
        self.user_repo = user_repo
        self.order_repo = order_repo

    async def execute(self, user_id: int) -> list[OrderEntity]:
        if not await self.user_repo.get_by_id(user_id):
            raise NotFound(detail=f"User {user_id} not found")

        return await self.order_repo.get_user_orders(user_id)
