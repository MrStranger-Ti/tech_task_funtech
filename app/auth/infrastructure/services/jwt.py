from datetime import timedelta, datetime, UTC
from typing import Any

import jwt

from app.auth.domain.entities import TokenType, TokenDataEntity
from app.auth.domain.interfaces.token_auth_provider import ITokenAuthProvider
from app.auth.domain.specifications import AuthTokenCreateSpec
from app.core.settings import settings


class JWTAuthProvider(ITokenAuthProvider):
    @property
    def token_type(self) -> str:
        return settings.auth.JWT_TYPE

    def create_access(self, token_data: AuthTokenCreateSpec) -> str:
        return self._encode_jwt(
            payload=token_data.model_dump(),
            exp=settings.auth.JWT_ACCESS_TOKEN_EXP_SECONDS,
            token_type=TokenType.ACCESS,
        )

    def read(self, token: str) -> TokenDataEntity | None:
        try:
            token_data = self._decode_jwt(
                token=token,
                secret_key=settings.auth.JWT_SECRET_KEY,
                algorithms=[settings.auth.JWT_ALGORITHM],
            )
        except jwt.PyJWTError:
            return None

        return TokenDataEntity.model_validate(token_data)

    def _encode_jwt(
        self,
        payload: dict[str, Any],
        exp: timedelta | int,
        token_type: TokenType,
        secret_key: str = settings.auth.JWT_SECRET_KEY,
        algorithm: str = settings.auth.JWT_ALGORITHM,
    ) -> str:
        prepared_payload = payload.copy()
        now = datetime.now(UTC)
        expire = (
            now + exp if isinstance(exp, timedelta) else now + timedelta(seconds=exp)
        )
        prepared_payload.update(
            iat=now.timestamp(),
            exp=expire.timestamp(),
            token_type=token_type.value,
        )

        return jwt.encode(
            payload=prepared_payload,
            key=secret_key,
            algorithm=algorithm,
        )

    def _decode_jwt(
        self,
        token: str,
        secret_key: str,
        algorithms: list[str],
    ) -> dict[str, Any] | None:
        return jwt.decode(
            jwt=token,
            key=secret_key,
            algorithms=algorithms,
        )
