from models.models import Category
from schemas.categories import CategoryCreateForm, CategoryUpdateForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, Depends, status


class CategoryService:
    @staticmethod
    async def all_categories(db: AsyncSession):

        result = await db.execute(select(Category))
        categories = result.scalars().all()

        if categories is None:
            raise HTTPException(status_code=404, detail="No categories")
        
        return categories
    

    @staticmethod
    async def create_category(db: AsyncSession, category_form: CategoryCreateForm):

        category_dict = category_form.dict()
        db_category = Category(**category_dict)

        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)
        return db_category
    

    @staticmethod
    async def get_category(db: AsyncSession, id: int):

        result = await db.execute(select(Category).filter(Category.id == id))
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(status_code=404, detail="No category")
        
        return category
    

    @staticmethod
    async def update_category(db: AsyncSession, category_form: CategoryUpdateForm, id):

        result = await db.execute(select(Category).filter(Category.id == id))
        db_category = result.scalar_one_or_none()
        if not db_category:
            raise HTTPException(status_code=404, detail="No such category")

        # db.add(db_category)
        await db.commit()  
        await db.refresh(db_category)
        return db_category