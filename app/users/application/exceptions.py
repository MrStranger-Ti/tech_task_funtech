from app.core.application.exceptions import ApplicationException


class InvalidCredentials(ApplicationException):
    detail = "Invalid credentials"
    code = "invalid_credentials"


class EmailAlreadyExists(ApplicationException):
    detail = "Email already exists"
    code = "email_already_exists"
