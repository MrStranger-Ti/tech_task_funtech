from fastapi import APIRouter

from app.users.presentation.api.v1.routes import router as users_router
from app.auth.presentation.api.v1.routes import router as auth_router
from app.orders.presentation.api.v1.routes import router as orders_router

router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(auth_router)
router.include_router(orders_router)
