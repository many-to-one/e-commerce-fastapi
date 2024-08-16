from passlib.context import CryptContext
from fastapi.security import HTTPBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()


def get_password_hash(password):
    return pwd_context.hash(password)