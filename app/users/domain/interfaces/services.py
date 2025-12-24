import abc


class IPasswordHasher(abc.ABC):
    @abc.abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abc.abstractmethod
    def check(self, password: str, hashed_password: str) -> bool:
        pass
