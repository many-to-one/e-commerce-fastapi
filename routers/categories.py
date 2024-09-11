from http.client import HTTPException
from typing import List
from core.security import get_current_user, check_admin
from db.database import get_db
from fastapi import APIRouter, Depends, Query, status
from models.models import Category
from orm.orm import OrmService
from schemas.users import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categories import CategoryBase, CategoryCreateForm, CategoryUpdateForm


router = APIRouter(tags=["Category"], prefix="/category")


@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[CategoryBase])
async def all_categories(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.all(model=Category, name='Categories')


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=CategoryBase)
async def create_category(
        category_form: CategoryCreateForm, #= Depends(CategoryCreateForm), 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.create(model=Category, form=category_form)


@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=CategoryBase)
async def get_category(
        id: int, 
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.get(id=id, model=Category, name='Category')


# Edit Category
@router.patch("/update/{id}", status_code = status.HTTP_200_OK, response_model=CategoryBase)
async def update_category(
        id: int,
        category_form: CategoryUpdateForm, #= Depends(CategoryUpdateForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.update(form=category_form, id=id, model=Category, name='Category')


@router.delete("/delete/{id}", status_code = status.HTTP_200_OK,)
async def delete_category(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)
    if current_user.is_admin == True:
        return await orm_service.delete(id=id, model=Category, name='Category')
    else:
        raise HTTPException(status_code=400, detail="Permission deny")