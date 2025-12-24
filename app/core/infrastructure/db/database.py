import contextlib
from typing import Any

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.settings import settings


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-1)

    def to_dict(self) -> dict[str, Any]:
        dict_attrs = {
            attr.key: getattr(self, attr.key) for attr in self.__mapper__.column_attrs  # type: ignore
        }
        return dict_attrs


class DbManger:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        autoflush: bool = True,
        autocommit: bool = False,
        expire_on_commit: bool = False,
    ):
        self.engine = create_async_engine(url, echo=echo)
        self.session_factory: async_sessionmaker = async_sessionmaker(
            bind=self.engine,
            autoflush=autoflush,
            autocommit=autocommit,
            expire_on_commit=expire_on_commit,
        )

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_manager = DbManger(
    url=settings.db.URL,
    echo=settings.db.ECHO,
    autoflush=settings.db.AUTOFLUSH,
    autocommit=settings.db.AUTOCOMMIT,
    expire_on_commit=settings.db.EXPIRED_ON_COMMIT,
)
