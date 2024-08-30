from typing import List
from fastapi import Body
from core.security import check_admin, get_current_user, get_password_hash
from db.database import get_db
from models.models import Cart
from orm.carts import CartService
from schemas.carts import *
from schemas.users import UserBase
from orm.orm import *

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Carts"], prefix="/cart")

@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[CartBase])
async def all_products(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.all(model=Cart, name='Cart')


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=CartBase)
async def create_cart(
        category_form: CartCreate = Depends(CartCreate), 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = CartService(db)
    return await orm_service.create_cart(model=Cart, form=category_form, user=current_user)


@router.get("/user", status_code=status.HTTP_200_OK, response_model=CartBase)
async def get_cart(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = CartService(db)
    return await orm_service.get_cart_by_user_id(id=current_user.id)


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=CartBase)
async def get_cart(
        id: int, 
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.get(id=id, model=Cart, name='Cart')


@router.patch("/update/{id}", status_code = status.HTTP_200_OK, response_model=CartBase)
async def update_cart(
        id: int,
        product_form: CartItemCreate = Body(...),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = CartService(db)
    return await orm_service.update_cart(form=product_form, id=id, model=Cart, name='Cart', user=current_user)


@router.patch("/cart_item/update", status_code = status.HTTP_200_OK, response_model=CartBase)
async def update_cart_item(
        product_form: CartItemUpdate = Body(...),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = CartService(db)
    return await orm_service.update_cart_item(form=product_form, model=Cart, name='Cart')


@router.delete("/delete_cart_item/{id}", status_code = status.HTTP_200_OK,)
async def delete_cart_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = CartService(db)
    if current_user.is_admin == True:
        return await orm_service.delete_cart_item(id=id, model=Cart, name='Cart')
    else:
        raise HTTPException(status_code=400, detail="Permission deny")
    

@router.delete("/delete/{id}", status_code = status.HTTP_200_OK,)
async def delete_product(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = CartService(db)
    if current_user.is_admin == True:
        return await orm_service.delete_cart(id=id, model=Cart, name='Cart')
    else:
        raise HTTPException(status_code=400, detail="Permission deny")