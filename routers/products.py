from typing import List
from core.security import check_admin, get_current_user, get_password_hash
from db.database import get_db
from models.models import Product, User
from schemas.products import *
from schemas.users import UserBase
from orm.orm import *
# from orm.redis_client import *
from redis_.redis import RedisClient
# from schemas.redis import Product

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Products"], prefix="/products")
client = RedisClient(host='redis', port=6379)

import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return super().default(obj)


# Use this encoder when dumping JSON
@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ProductBase])
async def all_products(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    redis_products = await client.get_value('Products')
    if redis_products:
        # print('######### redis_products exist #########', redis_products)
        return redis_products
    else:
        orm_service = OrmService(db)
        products = await orm_service.all(model=Product, name='Product')
        products_list = [ProductBase.from_orm(product).dict() for product in products]
        products_serialized_data = json.dumps(products_list, cls=CustomJSONEncoder)
        redis_products = await client.set_value('Products', products_serialized_data)
        # print('######### redis_products #########', products_serialized_data)
        return products_serialized_data
    


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ProductDisplay)
async def create_product(
        category_form: ProductCreateForm, 
        db: AsyncSession = Depends(get_db),
        check_admin: UserBase = Depends(check_admin),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    
    # Create a new product in the database
    bd_res = await orm_service.create(model=Product, form=category_form)
    
    # Serialize the new product for Redis storage
    new_product_ser = ProductBase.from_orm(bd_res).dict()

    # Fetch the existing list of products from Redis
    redis_products = await client.get_value('Products')

    if redis_products:
        # If products exist in Redis, load and append the new product
        if isinstance(redis_products, str):
            redis_products_list = json.loads(redis_products)  # Convert the JSON string to a Python list
        else:
            redis_products_list = redis_products  # Assume it's already a list

        # Append the new product to the list
        redis_products_list.append(new_product_ser)
        
        # Save the updated list back into Redis
        await client.set_value('Products', redis_products_list)
    else:
        # If no products exist in Redis, create a new list with the new product
        redis_products_list = [new_product_ser]
        
        # Save the new list in Redis
        await client.set_value('Products', redis_products_list)

    return new_product_ser




# @router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ProductBase])
# async def all_products(
#         db: AsyncSession = Depends(get_db),
#         current_user: UserBase = Depends(get_current_user)
#     ):
#     orm_service = OrmService(db)
    
#     # Fetch the existing list of products from Redis
#     redis_products = await client.get_value('Products')
    
#     if redis_products:
#         # If Redis returns a dictionary, ensure it's a list of products
#         if isinstance(redis_products, list):
#             return redis_products  # Redis already has a list, return it
        
#         redis_products_list = []
#         redis_products_list.append(redis_products)
#         return redis_products_list
    
#     # If Redis does not have products, fetch from the database
#     products = await orm_service.all(model=Product, name='Product')
    
    # # Cache the products in Redis
    # products_serialized = [ProductBase.from_orm(p).dict() for p in products]  # Prepare products list
    # await client.set_value('Products', products_serialized)  # Store the list directly, no JSON conversion
    
    # return products  # Return the list of products from the database





# @router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ProductDisplay)
# async def create_product(
#         category_form: ProductCreateForm, 
#         db: AsyncSession = Depends(get_db),
#         check_admin: UserBase = Depends(check_admin),
#         current_user: UserBase = Depends(get_current_user)
#     ):
#     orm_service = OrmService(db)
    
#     # Create a new product in the database
#     bd_res = await orm_service.create(model=Product, form=category_form)
    
#     # Serialize the new product for Redis storage
#     new_product_ser = ProductBase.from_orm(bd_res).dict()
#     new_product_serialized_data = json.dumps(new_product_ser, cls=CustomJSONEncoder)

#     # Fetch the existing list of categories from Redis
#     redis_products = await client.get_value('Products')
#     redis_products_list = []
    
#     if redis_products:
#         # new_product = await client.set_value('Products', new_product_serialized_data)
#         # redis_products_list = redis_products
#         redis_products_list.append(redis_products)
#         redis_products_list.append(new_product_serialized_data)
#         print('######### redis new_product added #########', redis_products_list)
#         return new_product_ser
#     else:
#         print('######### bd_res new_product #########', bd_res)
#         return bd_res




# @router.post("/new", status_code=status.HTTP_201_CREATED, response_model=ProductDisplay)
# async def create_product(
#         category_form: ProductCreateForm, 
#         db: AsyncSession = Depends(get_db),
#         check_admin: UserBase = Depends(check_admin),
#         current_user: UserBase = Depends(get_current_user)
#     ):
#     orm_service = OrmService(db)
    
#     # Create a new product in the database
#     bd_res = await orm_service.create(model=Product, form=category_form)
    
#     # Serialize the new product for Redis storage
#     new_product_ser = ProductBase.from_orm(bd_res).dict()

#     # Fetch the existing list of categories from Redis
#     cached_categories = await client.get_value('Categories')

#     # If cached_categories is already a list, use it; otherwise, initialize as empty list
#     if isinstance(cached_categories, list):
#         categories_list = cached_categories
#     elif cached_categories:  # If it's not a list, assume it's a JSON string
#         categories_list = cached_categories #json.loads(cached_categories)
#     else:
#         categories_list = []

#     # Check if the category exists in the Redis data
#     category_found = False
#     for category in categories_list:
#         if bd_res.category.name == category['name']:
#             # If the category exists, append the new product to the category's product list
#             category['products'].append(new_product_ser)
#             category_found = True
#             break
    
#     if not category_found:
#         # If the category is not found, create a new category entry with the new product
#         new_category = {
#             'name': bd_res.category.name,
#             'products': [new_product_ser]
#         }
#         categories_list.append(new_category)

#     # Store the updated categories list back into Redis
#     await client.set_value('Categories', categories_list) #json.dumps(categories_list)

#     return new_product_ser




# PROBABLY NOT USEABLE ROUTE
@router.get("/get/{id}", status_code=status.HTTP_200_OK, response_model=ProductDisplay)
async def get_product(
        id: int, 
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),       
    ):
    orm_service = OrmService(db)
    return await orm_service.get(id=id, model=Product, name='Product')



@router.patch("/update/{id}", status_code=status.HTTP_200_OK, response_model=ProductDisplay)
async def update_product(
        id: int,
        product_form: ProductUpdateForm, 
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)

    updated_product = await orm_service.update(form=product_form, id=id, model=Product, name='Product')

    updated_product_ser = ProductBase.from_orm(updated_product).dict()
    cached_products = await client.get_value('Products')
    
    if cached_products:
        # Find the product in the cached list and update it
        products_list = cached_products
        for index, product in enumerate(products_list):
            if product['id'] == id:
                products_list[index] = updated_product_ser
                break
        
        await client.set_value('Products', products_list)
    else:
        # If there's no cached product list, initialize one with the updated product
        products_list = [updated_product_ser]
        await client.set_value('Products', products_list)
    
    return updated_product_ser



@router.delete("/delete/{id}", status_code = status.HTTP_200_OK,)
async def delete_product(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)
    redis_products = await client.get_value('Products')

    if current_user.is_admin == True:
        # return await orm_service.delete(id=id, model=Product, name='Product')
        del_product = await orm_service.delete_product(id=id)
        if redis_products:
            redis_products_list = redis_products
            for product in redis_products_list:
                if product['id']== id:
                    redis_products_list.remove(product)
                    await client.set_value('Products', redis_products_list)
                    return redis_products_list
        else:
            return del_product

    else:
        raise HTTPException(status_code=400, detail="Permission deny")