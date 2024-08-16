from core.security import get_password_hash
from models.models import User
from schemas.auth import UserCreateForm
from sqlalchemy.ext.asyncio import AsyncSession
# from utils.responses import ResponseHandler


class AuthService:

    @staticmethod
    async def signup(db: AsyncSession, user_form: UserCreateForm):
        hashed_password = get_password_hash(user_form.password)
        db_user = User(
        username=user_form.username, 
        email=user_form.email, 
        password=hashed_password
    )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user