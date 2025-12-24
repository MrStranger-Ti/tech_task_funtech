from sqlalchemy.ext.asyncio import AsyncSession
from app.core.domain.interfaces.unit_of_work import IUnitOfWork


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._session.close()
        await self.rollback()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
