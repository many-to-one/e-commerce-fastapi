from typing import List
from core.security import check_admin, get_current_user, get_password_hash
from db.database import get_db
from models.models import User
from schemas.products import *
from schemas.users import UserBase
from services.products import ProductService

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[ProductDisplay])
async def all_categories(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    return await ProductService.all_products(db=db)


# Create New Category
@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ProductDisplay)
async def create_product(
        category_form: ProductCreateForm = Depends(ProductCreateForm), 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    return await ProductService.create_product(db, category_form)


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=ProductDisplay)
async def get_product(
        id: int, 
        db: AsyncSession = Depends(get_db),
        # check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    return await ProductService.get_product(db, id)


# Edit Category
@router.patch("/update/{id}", status_code = status.HTTP_200_OK, response_model=ProductDisplay)
async def update_product(
        id: int,
        category_form: ProductUpdateForm = Depends(ProductUpdateForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    
    return await ProductService.update_product(db, category_form, id)