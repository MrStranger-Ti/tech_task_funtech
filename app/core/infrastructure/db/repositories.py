import abc
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
