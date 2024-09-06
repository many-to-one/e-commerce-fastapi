from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from schemas.products import ProductDisplay, ProductBase


class CategoryBase(BaseModel):
    id: int
    name: str
    products: List[ProductBase] #Optional[List[ProductDisplay]] = []

    class Config:
        from_attributes = True


class CategoryCreateForm(BaseModel):
    name: str


class CategoryUpdateForm(BaseModel):
    name: str