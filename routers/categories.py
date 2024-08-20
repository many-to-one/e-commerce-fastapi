from typing import List
from core.security import get_current_user, check_admin
from db.database import get_db
from fastapi import APIRouter, Depends, Query, status
from schemas.users import UserBase
from services.categories import CategoryService
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categories import CategoryBase, CategoryCreateForm, CategoryUpdateForm


router = APIRouter(tags=["Category"], prefix="/category")


@router.get("/all_categories", status_code = status.HTTP_200_OK, response_model=List[CategoryBase])
async def all_categories(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    return await CategoryService.all_categories(db=db)


# Create New Category
@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryBase,
)
async def create_category(
        category_form: CategoryCreateForm = Depends(CategoryCreateForm), 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user),       
    ):
    return await CategoryService.create_category(db, category_form)


# Edit Category
@router.patch("/update_category/{id}", status_code = status.HTTP_200_OK, response_model=CategoryBase)
async def update_category(
        id: int,
        category_form: CategoryUpdateForm = Depends(CategoryUpdateForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    
    category = await CategoryService.update_category(db, category_form, id)
    if category_form.name is not None:
        category.name = category_form.name

    db.add(category)
    await db.commit()  
    await db.refresh(category)

    return category
