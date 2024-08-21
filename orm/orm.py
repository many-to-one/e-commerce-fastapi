from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, Depends, status

class OrmService:
    @staticmethod
    async def all(db: AsyncSession, model):

        result = await db.execute(select(model))
        categories = result.scalars().all()

        if categories is None:
            raise HTTPException(status_code=404, detail="No categories")
        
        return categories
    

    @staticmethod
    async def create(db: AsyncSession, model, category_form):

        product_dict = category_form.dict()
        product = model(**product_dict)

        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    

    @staticmethod
    async def get(db: AsyncSession, id: int, model):

        result = await db.execute(select(model).filter(model.id == id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="No product")
        
        return product
    

    @staticmethod
    async def update(db: AsyncSession, form, id, model):

        # result = await db.execute(select(Product).filter(Product.id == id))
        result = await db.execute(
        select(model).options(selectinload(model.category)).filter(model.id == id)
    )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="No such product")
        
        for field, value in form.dict().items():
            if value is not None:
                setattr(product, field, value)

        # db.add(db_category)
        await db.commit()  
        await db.refresh(product)
        return product