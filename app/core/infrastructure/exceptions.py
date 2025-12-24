from app.core.exceptions import AppException


class InfrastructureException(AppException):
    exc_type = "infrastructure"
    code = "infrastructure_layer_error"
    detail = "Error interacting with external services."


class ResponseValidationError(InfrastructureException):
    code = "validation_error"
    detail = "Some validation error from another service occurred."


class UnavailableError(InfrastructureException):
    code = "unavailable_error"
    detail = "Unavailable error occurred."


class ResponseTimeoutError(InfrastructureException):
    code = "response_timeout_error"
    detail = "Timeout error while waiting for response."
