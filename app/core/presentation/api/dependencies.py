from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.interfaces.cache import ICacheClient
from app.core.domain.interfaces.unit_of_work import IUnitOfWork
from app.core.infrastructure.cache.client import RedisClient
from app.core.infrastructure.cache.redis import redis_manager
from app.core.infrastructure.db.database import db_manager
from app.core.infrastructure.db.unit_of_work import SQLAlchemyUnitOfWork


async def get_session() -> AsyncSession:
    async with db_manager.get_session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_uow(session: AsyncSession = Depends(get_session)) -> IUnitOfWork:
    return SQLAlchemyUnitOfWork(session)


UOWDep = Annotated[IUnitOfWork, Depends(get_uow)]


async def get_cache_client() -> ICacheClient:
    yield RedisClient(conn=redis_manager.get_client())


CacheClientDep = Annotated[ICacheClient, Depends(get_cache_client)]
