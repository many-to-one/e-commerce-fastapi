from core.security import get_password_hash
from db.database import get_db
from models.models import User
from schemas.auth import UserBase, UserCreateForm
from services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Header


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/sing_up", response_model=UserBase)
async def sing_up(
        user_form: UserCreateForm = Depends(UserCreateForm), 
        db: AsyncSession = Depends(get_db)
    ):
    return await AuthService.signup(db=db, user_form=user_form)