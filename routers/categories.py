from http.client import HTTPException
from typing import List
from core.security import get_current_user, check_admin
from db.database import get_db
from fastapi import APIRouter, Depends, Query, status
from models.models import Category, Product, Subcategory
from orm.orm import OrmService
from redis_.redis import RedisClient
from schemas.products import ProductBase
from schemas.users import UserBase
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.categories import CategoryBase, CategoryCreateForm, CategoryUpdateForm, SubCategoryCreateForm


router = APIRouter(tags=["Category"], prefix="/category")
client = RedisClient(host='redis', port=6379)


import json
from datetime import datetime

# Use this encoder when dumping JSON
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return super().default(obj)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[CategoryBase])
async def all_categories(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.all(model=Category, name='Category')



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


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return super().default(obj)
    

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_category(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)
    default_category = await orm_service.get(id=44, model=Category, name="Category")
    print('######### default_category name #########', default_category.name)
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    category_to_delete = await orm_service.get(id=id, model=Category, name='Category')
    if not category_to_delete:
        raise HTTPException(status_code=404, detail="Category not found")
    
    products = await orm_service.all(model=Product, name='Product')
    for product in products:
        if product.category_id == id:
            product.category_id = default_category.id
            db.add(product) 
            await db.commit()
            await db.refresh(product)

    await client.delete_value('Products')
    products_list = [ProductBase.from_orm(product).dict() for product in products]
    products_serialized_data = json.dumps(products_list, cls=CustomJSONEncoder)
    await client.set_value('Products', products_serialized_data)


    # if category_to_delete.products:
    #     # Check if the "Default" category exists
    #     default_category = await orm_service.get(id=id, model=Category, name="Ogólna")

    #     # If "Default" category doesn't exist, create it
    #     if not default_category:
    #         default_category = await orm_service.create(
    #             model=Category,
    #             form={"name": "Ogólna"}  # Assuming form input is a dictionary or similar structure
    #         )

    #         print('^^^^^^^^ default_category ^^^^^^^^', default_category)
    #     print('^^^^^^^^ default_category exist ^^^^^^^^', default_category)

    #     for product in category_to_delete.products:
    #         # print('^^^^^^^^ product ++ ^^^^^^^^', product)
    #         product.category_id = default_category.id
    #         await db.add(product)  
    #         await db.commit()

    # redis_products = await client.get_value('Products')

    # Finally, delete the category
    await orm_service.delete(id=id, model=Category, name='Category')

    return {"detail": "Category deleted, and products reassigned to 'Default' category."}



# @router.delete("/delete/{id}", status_code = status.HTTP_200_OK,)
# async def delete_category(
#     id: int,
#     db: AsyncSession = Depends(get_db),
#     current_user: UserBase = Depends(get_current_user)
# ):
#     orm_service = OrmService(db)
#     if current_user.is_admin == True:
#         return await orm_service.delete(id=id, model=Category, name='Category')
#     else:
#         raise HTTPException(status_code=400, detail="Permission deny")



# Create a new subcategory under a specific category
@router.post("/{category_id}/subcategories", status_code=status.HTTP_201_CREATED, response_model=SubcategoryDisplay)
async def create_subcategory(
    category_id: int, 
    subcategory: SubCategoryCreateForm, 
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)

    # Only admin users can create subcategories
    if current_user.is_admin:
        category = await orm_service.get_by_id(id=category_id, model=Category)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        subcategory_data = subcategory.dict()
        subcategory_data["category_id"] = category_id
        new_subcategory = await orm_service.create(model=Subcategory, form=subcategory_data)
        return new_subcategory
    else:
        raise HTTPException(status_code=403, detail="Not authorized")