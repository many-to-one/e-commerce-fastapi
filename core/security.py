# import datetime
from datetime import datetime, timedelta, timezone
from db.database import get_db
from fastapi import HTTPException, status
from jose import JWTError, jwt
from core.config import settings
from passlib.context import CryptContext
# from fastapi.security import HTTPBearer
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends
from models.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.auth import TokenResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# auth_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


# Verify Hash Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create Access & Refresh Token
async def get_user_token(db, id: int, refresh_token=None):
    payload = {"id": id}
    # print('********* id **********', id)

    access_token_expiry = timedelta(minutes=settings.access_token_expire_minutes)

    access_token = await create_access_token(payload, access_token_expiry)
    result = await db.execute(select(User).filter(User.id == id))
    user = result.scalar_one_or_none()
    user.access_token = access_token
    db.add(user)
    await db.commit()
    await db.refresh(user)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(
        id=id,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )


# Create Access Token
async def create_access_token(data: dict, access_token_expiry=None):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# Create Refresh Token
async def create_refresh_token(data):
    return jwt.encode(data, settings.secret_key, settings.algorithm)


# Get Payload Of Token
async def get_token_payload(token: str)-> dict:
    try:
        return jwt.decode(token, settings.secret_key, [settings.algorithm])
    except JWTError:
        # raise ResponseHandler.invalid_token('access')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

# token: str = Depends(oauth2_scheme) for Swagger Authorize
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db))-> User:
    # print('********* token **********', token)
    user = await get_token_payload(token)
    user_id = user.get('id')
    result = await db.execute(select(User).filter(User.id == user_id))
    current_user = result.scalar_one_or_none()
    # return user.get('id')
    return current_user


async def check_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):

    user = await get_token_payload(token)
    user_id = user.get('id')
    result = await db.execute(select(User).filter(User.id == user_id))
    current_user = result.scalar_one_or_none()
    if current_user.is_admin != True:
        raise HTTPException(status_code=403, detail="Admin role required")