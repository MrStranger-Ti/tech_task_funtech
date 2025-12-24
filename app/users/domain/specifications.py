from app.core.domain.specifications import Specification


class UserCreateSpec(Specification):
    email: str
    password: str
