from app.core.application.exceptions import ApplicationException


class InvalidToken(ApplicationException):
    detail = "Invalid token"
    code = "invalid_token"
