from models.models import Cart, CartItem, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, Depends, status

class OrmService:
    def __init__(self, db):
        self.db = db
        
    async def all(self, model, name):

        result = await self.db.execute(select(model))
        obj = result.scalars().all()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        return obj
    

    async def create(self, model, form):

        obj_dict = form.dict()
        obj = model(**obj_dict)

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    

    async def get(self, id: int, model, name):

        result = await self.db.execute(select(model).filter(model.id == id))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        return obj
    

    async def update(self, form, id, model, name):

        if model == Product:
            result = await self.db.execute(
                select(model).options(selectinload(model.category)).filter(model.id == id)
            )
            obj = result.scalar_one_or_none()
        else:
            obj = await self.get(id=id, model=model, name=name)
    
        if not obj:
            raise HTTPException(status_code=404, detail=f"No such {name}")
        
        for field, value in form.dict().items():
            if value is not None:
                setattr(obj, field, value)

        await self.db.commit()  
        await self.db.refresh(obj)
        return obj
    

    async def delete(self, id: str, model, name):

        result = await self.db.execute(select(model).filter(model.id == id))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        await self.db.delete(obj)
        await self.db.commit()
        await self.db.flush()
        
        return {
            "message": f"{name} deleted successfully!",
            "userMessage": f"Objekt {name} został usunięty!",
            }