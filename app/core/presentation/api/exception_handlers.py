import logging
import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.auth.presentation.exceptions import NotAuthorized
from app.core.application.exceptions import NotFound
from app.users.application.exceptions import EmailAlreadyExists, InvalidCredentials

log = logging.getLogger(__name__)

EXCEPTION_HTTP_STATUS_MAPPING = {
    status.HTTP_400_BAD_REQUEST: [
        EmailAlreadyExists,
    ],
    status.HTTP_401_UNAUTHORIZED: [
        InvalidCredentials,
        NotAuthorized,
    ],
    status.HTTP_404_NOT_FOUND: [
        NotFound,
    ],
}


def _get_optimized_mapping(
    mappings: dict[int, list[type[Exception]]]
) -> dict[type[Exception], int]:
    return {
        exc: status_code
        for status_code, excs_types in mappings.items()
        for exc in excs_types
    }


_OPTIMIZED_EXCEPTION_HTTP_STATUS_MAPPING = _get_optimized_mapping(
    EXCEPTION_HTTP_STATUS_MAPPING,
)


def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if status_code := _OPTIMIZED_EXCEPTION_HTTP_STATUS_MAPPING.get(type(exc)):
        return JSONResponse(
            content=dict(
                detail=exc.detail,
                code=exc.code,
                **exc.extra,
            ),
            status_code=status_code,
        )

    traceback_strings = traceback.format_exception(type(exc), exc, exc.__traceback__)
    log.error("".join(traceback_strings))

    return JSONResponse(
        content={
            "detail": "Internal Server Error",
            "code": "internal_server_error",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
