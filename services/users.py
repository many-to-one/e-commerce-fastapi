from core.security import get_password_hash, get_user_token, verify_password
from db.database import get_db
from models.models import User
from schemas.users import UserCreateForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends, status


class UserService:
    @staticmethod
    async def all_users(db: AsyncSession):

        result = await db.execute(select(User))
        users = result.scalars().all()

        if users is None:
            raise HTTPException(status_code=404, detail="No users")
        
        return users
    

    @staticmethod
    async def get_user(db: AsyncSession, id: str):

        result = await db.execute(select(User).filter(User.id == id))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="No user")
        
        return user
    

    @staticmethod
    async def delete_user(db: AsyncSession, id: str):

        result = await db.execute(select(User).filter(User.id == id))
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="No user")
        
        await db.delete(user)
        await db.commit()
        await db.flush()
        
        return {"message": "User deleted successfully!"}