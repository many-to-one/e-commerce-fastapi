from http.client import HTTPException
from typing import List
from core.security import get_current_user, check_admin
from db.database import get_db
from fastapi import APIRouter, Depends, Query, status
from models.models import Category
from orm.orm import OrmService
from redis_.redis import RedisClient
from schemas.users import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categories import CategoryBase, CategoryCreateForm, CategoryUpdateForm


router = APIRouter(tags=["Category"], prefix="/category")
client = RedisClient(host='redis', port=6379)


import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return super().default(obj)

# Use this encoder when dumping JSON
@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[CategoryBase])
async def all_products(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    result = await orm_service.all(model=Category, name='Category')

    # Serialize the result using Pydantic models
    all_cached_categories_ser = [CategoryBase.from_orm(product).dict() for product in result]

    # Check if products are in Redis
    cached_categories = await client.get_value('Categories')

    if cached_categories:
        print('************ REDIS cached_categories ***********', cached_categories)
        return cached_categories
    else:
        # Serialize the result with custom JSON encoder
        serialized_data = json.dumps(all_cached_categories_ser, cls=CustomJSONEncoder)
        await client.set_value('Categories', serialized_data)
        print('************ REDIS ALL Category ***********', await client.get_value('Categories'))
        return all_cached_categories_ser


# @router.get("/all", status_code = status.HTTP_200_OK, response_model=List[CategoryBase])
# async def all_categories(
#         db: AsyncSession = Depends(get_db),
#         current_user: UserBase = Depends(get_current_user)
#     ):
#     orm_service = OrmService(db)
#     return await orm_service.all(model=Category, name='Categories')


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