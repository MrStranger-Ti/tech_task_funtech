from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.auth.presentation.api.dependancies import CurrentUserDep
from app.auth.presentation.api.permissions import is_authenticated
from app.orders.application.dtos import OrderReadDTO, OrderCreateDTO, OrderUpdateDTO
from app.orders.presentation.api.dependencies import (
    OrderCreateUCDep,
    OrderGetUCDep,
    OrderUpdateUCDep,
    UserOrdersUCDep,
)
from app.users.domain.entities import UserEntity

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=OrderReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authorized",
        },
    },
)
async def create_order(
    current_user: Annotated[UserEntity, Depends(is_authenticated)],
    dto: OrderCreateDTO,
    uc: OrderCreateUCDep,
):
    return await uc.execute(dto=dto, user_id=current_user.id)


@router.get(
    "/{order_id}/",
    response_model=OrderReadDTO,
    summary="Get order by id",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
    },
)
async def get_order(order_id: int, uc: OrderGetUCDep):
    return await uc.execute(order_id)


@router.patch(
    "/{order_id}/",
    response_model=OrderReadDTO,
    summary="Update order",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Order not found"},
    },
)
async def update_order(order_id: int, dto: OrderUpdateDTO, uc: OrderUpdateUCDep):
    return await uc.execute(order_id, dto)


@router.get(
    "/user/{user_id}/",
    response_model=list[OrderReadDTO],
    summary="Get user's orders",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_user_orders(user_id: int, uc: UserOrdersUCDep):
    return await uc.execute(user_id)
