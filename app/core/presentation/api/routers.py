from fastapi import APIRouter

from app.core.presentation.api.v1.routers import router as v1_router

main_router = APIRouter(prefix="/api")

main_router.include_router(v1_router)
