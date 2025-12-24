import redis
from redis.asyncio import Redis

from app.core.settings import settings


class RedisManager:
    def __init__(
        self,
        url: str,
        decode_responses: bool = True,
        encoding: str = "utf-8",
    ) -> None:
        self.url: str = url
        self.encoding: str = encoding
        self.decode_responses: bool = decode_responses

    def _get_conn(self) -> Redis:
        return redis.asyncio.from_url(
            url=self.url,
            decode_responses=self.decode_responses,
            encoding=self.encoding,
        )

    def get_client(self) -> Redis:
        return self._get_conn()


redis_manager = RedisManager(
    url=settings.cache.REDIS_URL,
    decode_responses=settings.cache.REDIS_DECODE_RESPONSES,
    encoding=settings.cache.REDIS_ENCODING,
)
