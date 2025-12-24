from app.core.exceptions import AppException


class PresentationException(AppException):
    detail = "presentation error"
    code = "presentation_error"
