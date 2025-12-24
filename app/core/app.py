from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

from app.core.infrastructure.broker.taskiq import configure_tasks_dependencies, broker
from app.core.logging import configure_logging
from app.core.presentation.api.exception_handlers import app_exception_handler
from app.core.presentation.api.routers import main_router
from app.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await broker.startup()
    yield
    await broker.shutdown()


def create_app() -> FastAPI:
    """
    Creating FastAPI application.

    Adding main router, base exception handler for every exception and middlewares.

    :return: FastAPI
    """
    configure_logging()

    app = FastAPI(
        title="Order management service",
        description="This service can manage orders and order items. Includes registration, login and simple JWT authorization.",
        lifespan=lifespan,
    )

    app.include_router(main_router)

    app.add_exception_handler(Exception, app_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH"],
        allow_headers=["*"],
    )

    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=settings.server.LIMITER_STORAGE_URI,
        default_limits=[f"{settings.server.LIMITER_REQ_PER_MIN}/minute"]
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    configure_tasks_dependencies(app)

    return app
