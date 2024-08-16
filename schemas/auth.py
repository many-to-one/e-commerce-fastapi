from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    # is_active: bool
    # created_at: datetime


class UserCreateForm(BaseModel):
    username: str
    email: EmailStr
    password: str