from app.core.exceptions import AppException


class ApplicationException(AppException):
    exc_type = "application"
    code = "application_layer_exception"
    detail = "Business logic orchestration error."


class NotFound(ApplicationException):
    detail = "Not found"
    code = "not_found"
