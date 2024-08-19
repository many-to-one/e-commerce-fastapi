from core.security import get_password_hash, get_user_token, verify_password
from db.database import get_db
from models.models import User
from schemas.auth import UserCreateForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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
    

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str):
        result = await db.execute(select(User).filter(User.username == username))  # Await the query execution
        user = result.scalar_one_or_none()  # Get one user or none
        print('********* User **********', user.id, user.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        return await get_user_token(id=user.id)
    
    @staticmethod
    async def all_users(db: AsyncSession):

        result = await db.execute(select(User))
        users = result.scalars().all()

        if users is None:
            raise HTTPException(status_code=404, detail="No users")
        
        return users