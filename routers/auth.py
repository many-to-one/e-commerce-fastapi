from typing import List
from core.security import get_current_user, get_password_hash
from db.database import get_db
from models.models import User
from schemas.auth import TokenResponse, UserBase, UserCreateForm
from services.auth import AuthService

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Header
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Auth"], prefix="/auth")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/sing_up", response_model=UserBase)
async def sing_up(
        user_form: UserCreateForm = Depends(UserCreateForm), 
        db: AsyncSession = Depends(get_db)
    ):
    return await AuthService.signup(db=db, user_form=user_form)


@router.post("/login", response_model=TokenResponse)
async def login(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db),
    ):
    print('********* user_credentials **********', user_credentials)
    return await AuthService.login(db, user_credentials.username, user_credentials.password)


@router.get("/all_users", response_model=List[UserBase])
async def all_users(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    return await AuthService.all_users(db=db)
    # return await AuthService.all_users(db=db)