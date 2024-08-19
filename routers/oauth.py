from typing import List
from core.security import get_password_hash
from db.database import get_db
from models.models import User
from schemas.auth import TokenResponse, UserBase, UserCreateForm
from services.auth import AuthService

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Header, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #from fastapi.security.oauth2

router = APIRouter()

@router.post("/token", response_model=TokenResponse)
async def token(
        request: Request,
        response: Response,
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
    ):
    return await AuthService.login(db=db, user_credentials=user_credentials)