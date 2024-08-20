from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class CategoryBase(BaseModel):
    id: int
    name: str


class CategoryCreateForm(BaseModel):
    name: str


class CategoryUpdateForm(BaseModel):
    name: str