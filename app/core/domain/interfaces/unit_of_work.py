import abc
from typing import Self


class IUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abc.abstractmethod
    async def __aexit__(self, *args):
        pass

    @abc.abstractmethod
    async def commit(self):
        pass

    @abc.abstractmethod
    async def rollback(self):
        pass
