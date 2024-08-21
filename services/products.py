from models.models import Product
from schemas.products import ProductCreateForm, ProductUpdateForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, Depends, status


class ProductService:
    @staticmethod
    async def all_products(db: AsyncSession):

        result = await db.execute(select(Product))
        categories = result.scalars().all()

        if categories is None:
            raise HTTPException(status_code=404, detail="No categories")
        
        return categories
    

    @staticmethod
    async def create_product(db: AsyncSession, category_form: ProductCreateForm):

        product_dict = category_form.dict()
        product = Product(**product_dict)

        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    

    @staticmethod
    async def get_product(db: AsyncSession, id: int):

        result = await db.execute(select(Product).filter(Product.id == id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(status_code=404, detail="No product")
        
        return product
    

    @staticmethod
    async def update_product(db: AsyncSession, product_form: ProductUpdateForm, id):

        # result = await db.execute(select(Product).filter(Product.id == id))
        result = await db.execute(
        select(Product).options(selectinload(Product.category)).filter(Product.id == id)
    )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="No such product")
        
        for field, value in product_form.dict().items():
            if value is not None:
                setattr(product, field, value)

        # db.add(db_category)
        await db.commit()  
        await db.refresh(product)
        return product