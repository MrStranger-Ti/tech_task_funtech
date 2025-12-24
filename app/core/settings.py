from pathlib import Path

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    PROTOCOL: str = "http"
    HOST: str = "localhost"
    PORT: int = 8000
    ALLOW_ORIGINS: list[str] = Field(default_factory=list)
    LIMITER_STORAGE_URI: str = "memory://"
    LIMITER_REQ_PER_MIN: int = 20
    LOGGING_LEVEL: str = "INFO"

    @computed_field
    @property
    def SOURCE(self) -> str:
        return f"{self.PROTOCOL}://{self.HOST}:{self.PORT}"


class AuthSettings(BaseModel):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_TYPE: str = "Bearer"
    JWT_ACCESS_TOKEN_EXP_SECONDS: int = 60 * 60 * 24 * 7


class DbSettings(BaseModel):
    # Connection
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str
    DRIVER: str = "postgresql+asyncpg"

    # Sqlalchemy
    ECHO: bool = False
    AUTOFLUSH: bool = True
    AUTOCOMMIT: bool = False
    EXPIRED_ON_COMMIT: bool = False

    @computed_field
    @property
    def URL(self) -> str:
        return f"{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class BrokerSettings(BaseModel):
    KAFKA_HOST: str
    KAFKA_PORT: int

    @computed_field
    @property
    def KAFKA_URL(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class CacheSettings(BaseModel):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_DECODE_RESPONSES: bool = True
    REDIS_ENCODING: str = "utf-8"
    REDIS_DEFAULT_TTL: int = 60 * 5

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    server: ServerSettings = Field(default_factory=ServerSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    db: DbSettings = Field(default_factory=DbSettings)
    broker: BrokerSettings = Field(default_factory=BrokerSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
