from models.models import Cart, CartItem, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, Depends, status
from orm.orm import OrmService


class CartService:
    def __init__(self, db):
        self.db = db

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
            product = await OrmService(self.db).get(id=cart_items_data[0]['product_id'], model=Product, name='Product')
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
    

    async def get_cart_by_user_id(self, id):

        result = await self.db.execute(
            select(Cart)
            .filter(Cart.user_id == id)
            .options(joinedload(Cart.cart_items).selectinload(CartItem.product))
        )
        result = result.unique()
        cart = result.scalar_one_or_none()

        if cart is None:
            raise HTTPException(status_code=404, detail="No cart found for this user")
        
        return cart
    

    async def update_cart_item(self, form, cart_id, cart_item_id, model, name):

        total_amount = 0
        cart = await OrmService(self.db).get(id=cart_id, model=model, name=name)
        if not cart:
            raise HTTPException(status_code=404, detail=f"No such {name}")
        cartItem = await OrmService(self.db).get(id=cart_item_id, model=CartItem, name='CartItem')
        if not cartItem:
            raise HTTPException(status_code=404, detail=f"No such cartItem")

                
        for field, value in form.dict().items():
            # print('***** update_cart obj_dict *****', field, value)
            if value is not None:
                setattr(cartItem, field, value)

        await self.db.commit()  
        await self.db.refresh(cartItem)

        for item in cart.cart_items:
            item.subtotal = item.quantity * item.product.price
            total_amount += item.subtotal
            # print('***** item.subtotal *****', item.subtotal)
        cart.total_amount = total_amount

        await self.db.commit()  
        await self.db.refresh(cart)
        return cart
    

    async def update_cart(self, form, id, model, name, user):

        total_amount = 0
        cart = await OrmService(self.db).get(id=id, model=model, name=name)
        product = await OrmService(self.db).get(id=form.product_id, model=Product, name='Product')
        subtotal = product.price * form.quantity
        cart_item = CartItem(
                product_id=form.product_id,
                quantity=form.quantity,
                subtotal=subtotal
            )
        cart.cart_items.append(cart_item)

        for item in cart.cart_items:
            total_amount += item.subtotal
            print('***** item.subtotal *****', item.subtotal)
        cart.total_amount = total_amount
       

        if not cart:
            raise HTTPException(status_code=404, detail=f"No such {name}")
                
        await self.db.commit()  
        await self.db.refresh(cart)
        return cart
    

    async def delete_cart_item(self, id: int, model, name):
    # Fetch the CartItem by ID
        result = await self.db.execute(
            select(CartItem)
            .filter(CartItem.id == id)
            .options(joinedload(CartItem.product))  # Optionally load related product if needed
        )
        cart_item = result.scalar_one_or_none()

        # Check if the CartItem exists
        if cart_item is None:
            raise HTTPException(status_code=404, detail="CartItem not found")

        # Delete the CartItem
        await self.db.delete(cart_item)
        await self.db.commit()
        await self.db.flush()
        
        return {
            "message": "CartItem deleted successfully!",
            "userMessage": "Pozycja w koszyku została usunięta!"
        }



    async def delete_cart(self, id: str, model, name):

        result = await self.db.execute(
            select(model)
            .options(joinedload(Cart.cart_items).joinedload(CartItem.product))
            .filter(model.id == id))
        result = result.unique()
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name} with id {id}")
        
        for cart_item in obj.cart_items:
            await self.db.delete(cart_item)
        
        
        await self.db.delete(obj)
        await self.db.commit()
        await self.db.flush()
        
        return {
            "message": f"{name} with id {id} deleted successfully!",
            "userMessage": f"Koszyk został usunięty!",
            }