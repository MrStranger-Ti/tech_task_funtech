from app.core.presentation.exeptions import PresentationException


class NotAuthorized(PresentationException):
    detail = "Not authenticated"
    code = "not_authenticated"
