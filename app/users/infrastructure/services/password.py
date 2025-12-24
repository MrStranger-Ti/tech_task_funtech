import bcrypt

from app.users.domain.interfaces.services import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")

    def check(self, password: str, hashed_password: str) -> bool:
        pwd_bytes = password.encode("utf-8")
        hashed_pwd_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hashed_pwd_bytes)
