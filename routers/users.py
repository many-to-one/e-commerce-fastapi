from typing import List
from core.security import get_current_user, get_password_hash
from db.database import get_db
from models.models import User
from orm.orm import OrmService
from schemas.users import UserBase, UserCreateForm, UserEditForm

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[UserBase])
async def all_users(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.all(model=User, name='User')


@router.get("/me", status_code = status.HTTP_200_OK, response_model=UserBase)
async def get_me(
        current_user: UserBase = Depends(get_current_user)
    ):
    print(' ***** user *****', current_user)
    return current_user


@router.get("/{id}", status_code = status.HTTP_200_OK, response_model=UserBase)
async def get_user(
        id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.get(id=id, model=User, name='User')



@router.patch("/update/{id}", status_code = status.HTTP_200_OK, response_model=UserBase)
async def update_user(
    id: int,
        user_form: UserEditForm = Depends(UserEditForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    orm_service = OrmService(db)
    return await orm_service.update(form=user_form, id=id, model=User, name='User')


@router.delete("/delete_by_id/{id}", status_code = status.HTTP_200_OK,)
async def delete_user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    orm_service = OrmService(db)
    if current_user.is_admin == True:
        return await orm_service.delete(id=id, model=User, name='User')
    else:
        raise HTTPException(status_code=400, detail="Permission deny")
    

@router.delete("/delete_user_by_himself", status_code = status.HTTP_200_OK,)
async def delete_user_by_himself(
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
     orm_service = OrmService(db)
     return await orm_service.delete(id=current_user.id, model=User, name='User') 
