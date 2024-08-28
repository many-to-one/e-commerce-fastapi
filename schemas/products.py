from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# from schemas.categories import CategoryBase


class ProductBase(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    rating: Optional[float] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None
    images: List[str]
    is_published: bool
    created_at: datetime


class ProductDisplay(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    category_id: int
    thumbnail: str
    # category: Optional[CategoryBase]

    class Config:
        from_attributes = True


class ProductCreateForm(BaseModel):
    title: str
    price: float
    stock: int
    category_id: int
    discount_percentage: Optional[float] = None
    rating: Optional[float] = None
    brand: Optional[str] = None
    thumbnail: Optional[str] = None
    images: Optional[List[str]] = None


class ProductUpdateForm(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None