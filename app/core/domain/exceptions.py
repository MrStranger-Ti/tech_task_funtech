from app.core.exceptions import AppException


class DomainException(AppException):
    exc_type = "domain"
    code = "domain_layer_exception"
    detail = "Incorrect business logic."
