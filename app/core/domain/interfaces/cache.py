import abc
from typing import Any


class ICacheClient(abc.ABC):
    @abc.abstractmethod
    async def set(self, key: str, value: Any, time: Any = None) -> None:
        pass

    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        pass

    @abc.abstractmethod
    async def clear_all(self) -> None:
        pass
