import re
from core.security import get_password_hash, get_user_token, verify_password
from db.database import get_db
from models.models import User
from schemas.users import UserCreateForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Response, status


class AuthService:

    @staticmethod
    async def signup(db: AsyncSession, user_form: UserCreateForm):
        hashed_password = get_password_hash(user_form.password)
        db_user = User(
        username=user_form.username, 
        email=user_form.email, 
        password=hashed_password,
        is_active=False,
    )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str, response):
        result = await db.execute(select(User).filter(User.username == username))  # Await the query execution
        user = result.scalar_one_or_none() 
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        user.is_active = True
        await db.commit()

        return await get_user_token(db=db, id=user.id)
    

    @staticmethod
    async def change_password(db: AsyncSession, current_user, old_password: str, new_password: str):

        if not current_user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(old_password, current_user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        hashed_password = get_password_hash(new_password)
        current_user.password = hashed_password
        await db.commit()
        
        return current_user