from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from schemas.categories import CategoryBase
from schemas.products import ProductBase


# Base Cart & Cart_Item
class CartItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: ProductBase

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: List[CartItemBase]

    class Config:
        from_attributes = True


# class CartItems(BaseModel):
#     product_id: int
#     quantity: int

# Update Cart
class CartItemUpdate(BaseModel):
    cart_id: int
    cart_item_id: int
    product_id: int
    quantity: int


# Create Cart
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartCreate(BaseModel):
    cart_items: List[CartItemCreate]