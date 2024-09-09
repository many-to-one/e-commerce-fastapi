from typing import List
from core.security import check_admin, get_current_user, get_password_hash
from db.database import get_db
from models.models import Product, User
from schemas.products import *
from schemas.users import UserBase
from orm.orm import *

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Products"], prefix="/products")

@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[ProductBase])
async def all_products(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.all(model=Product, name='Product')


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ProductDisplay)
async def create_product(
        category_form: ProductCreateForm, #= Depends(ProductCreateForm), 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.create(model=Product, form=category_form)


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=ProductDisplay)
async def get_product(
        id: int, 
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.get(id=id, model=Product, name='Product')


@router.patch("/update/{id}", status_code = status.HTTP_200_OK, response_model=ProductDisplay)
async def update_product(
        id: int,
        product_form: ProductUpdateForm, #= Depends(ProductUpdateForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.update(form=product_form, id=id, model=Product, name='Product')


@router.delete("/delete/{id}", status_code = status.HTTP_200_OK,)
async def delete_product(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)
    if current_user.is_admin == True:
        # return await orm_service.delete(id=id, model=Product, name='Product')
        return await orm_service.delete(id=id)
    else:
        raise HTTPException(status_code=400, detail="Permission deny")