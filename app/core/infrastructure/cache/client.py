import json
from datetime import timedelta

from redis.asyncio import Redis

from app.core.domain.interfaces.cache import ICacheClient


class RedisClient(ICacheClient):
    def __init__(self, conn: Redis) -> None:
        self.conn: Redis = conn

    async def set(
        self,
        key: str,
        value: list | dict,
        time: int | timedelta | None = None,
    ) -> None:
        serialized = self._serialize(value)
        if time is None:
            await self.conn.set(name=key, value=serialized)
        else:
            await self.conn.setex(name=key, value=serialized, time=time)

    async def get(self, key: str) -> list | dict | None:
        serialized = await self.conn.get(name=key)
        if serialized is None:
            return None

        return self._deserialize(serialized)

    async def clear_all(self) -> None:
        await self.conn.flushdb()

    def _serialize(self, value: list | dict) -> str:
        return json.dumps(value)

    def _deserialize(self, value: str) -> list | dict:
        return json.loads(value)
