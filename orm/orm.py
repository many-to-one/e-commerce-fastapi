from models.models import Cart, CartItem, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
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
    


    async def create_cart(self, model, form, user):
        print('***** form *****', form)
        obj_dict = form.dict()
        print('***** form obj_dict *****', obj_dict)

        # Extract and remove cart_items from the form data
        cart_items_data = obj_dict.pop('cart_items', [])
        print('***** form cart_items_data *****', cart_items_data)

        total_amount = 0

        # Initialize cart items and calculate total amount
        cart_items = []
        for item_data in cart_items_data:
            product = await self.get(id=cart_items_data[0]['product_id'], model=Product, name='Product')
            subtotal = product.price * item_data['quantity']
            total_amount += subtotal

            # Create CartItem object
            cart_item = CartItem(
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                subtotal=subtotal
            )
            cart_items.append(cart_item)

        # Create Cart object with the calculated total amount and cart items
        obj_cart = Cart(
            user_id=user.id,
            total_amount=total_amount,
            cart_items=cart_items
        )

        # Add the Cart object to the database
        self.db.add(obj_cart)
        await self.db.commit()
        await self.db.refresh(obj_cart)

        return obj_cart
    

    async def update_cart(self, form, id, model, name):

        cart = await self.get(id=id, model=model, name=name)
        for cart_item in cart.cart_items:
            print('***** cart_item product price *****', cart_item.product.price)
            print('***** cart_item quantity *****', cart_item.quantity)
            print('***** cart_item subtotal *****', cart_item.subtotal)
            cartItem = await self.get(id=cart_item.id, model=CartItem, name='CartItem')
            cartItem.subtotal = cart_item.quantity * cart_item.product.price
    
        if not cart:
            raise HTTPException(status_code=404, detail=f"No such {name}")
                
        for field, value in form.dict().items():
            print('***** update_cart obj_dict *****', field, value)
            if value is not None:
                setattr(cartItem, field, value)
        cartItem.subtotal = cart_item.quantity * cart_item.product.price

        await self.db.commit()  
        await self.db.refresh(cartItem)
        return cart

    

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