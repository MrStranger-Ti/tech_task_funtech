from typing import Any


class AppException(Exception):
    exc_type: str = "base"
    code: str = "application_exception"
    detail: str = "The application has an error."
    extra: dict[str, Any] | None = None

    def __init__(
        self,
        detail: str | None = None,
        exc_type: str | None = None,
        code: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.detail: str = detail or self.detail
        self.exc_type: str = exc_type or self.exc_type
        self.code: str = code or self.code
        self.extra: dict[str, Any] = extra or self.extra or {}
        super().__init__(self.detail)
