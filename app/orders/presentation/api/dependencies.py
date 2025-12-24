from typing import Annotated

from fastapi import Depends

from app.core.presentation.api.dependencies import DBSessionDep, UOWDep, CacheClientDep
from app.core.settings import settings
from app.orders.application.use_cases import (
    OrderCreateUC,
    OrderGetUC,
    OrderUpdateUC,
    UserOrdersUC,
)
from app.orders.domain.interfaces.repositories import IOrderRepository
from app.orders.infrastructure.db.repositories import OrderRepository
from app.users.presentation.api.dependencies import UserRepoDep


def get_order_repo(session: DBSessionDep) -> IOrderRepository:
    return OrderRepository(session)


OrderRepoDep = Annotated[IOrderRepository, Depends(get_order_repo)]


def get_order_create_uc(uow: UOWDep, order_repo: OrderRepoDep) -> OrderCreateUC:
    return OrderCreateUC(
        uow=uow,
        order_repo=order_repo,
    )


OrderCreateUCDep = Annotated[OrderCreateUC, Depends(get_order_create_uc)]


def get_order_get_uc(
    cache_client: CacheClientDep,
    order_repo: OrderRepoDep,
) -> OrderGetUC:
    return OrderGetUC(
        cache_client=cache_client,
        order_repo=order_repo,
        cache_ttl=settings.cache.REDIS_DEFAULT_TTL,
    )


OrderGetUCDep = Annotated[OrderGetUC, Depends(get_order_get_uc)]


def get_order_update_uc(
    uow: UOWDep,
    cache_client: CacheClientDep,
    order_repo: OrderRepoDep,
) -> OrderUpdateUC:
    return OrderUpdateUC(
        uow=uow,
        cache_client=cache_client,
        order_repo=order_repo,
        cache_ttl=settings.cache.REDIS_DEFAULT_TTL,
    )


OrderUpdateUCDep = Annotated[
    OrderUpdateUC,
    Depends(get_order_update_uc),
]


def get_user_orders_get_uc(
    user_repo: UserRepoDep,
    order_repo: OrderRepoDep,
) -> UserOrdersUC:
    return UserOrdersUC(
        user_repo=user_repo,
        order_repo=order_repo,
    )


UserOrdersUCDep = Annotated[UserOrdersUC, Depends(get_user_orders_get_uc)]
