from typing import List
from core.security import get_current_user, get_password_hash
from db.database import get_db
from models.models import User
from schemas.users import UserBase, UserCreateForm, UserEditForm
from services.users import UserService

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response


router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/all", status_code = status.HTTP_200_OK, response_model=List[UserBase])
async def all_users(
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    return await UserService.all_users(db=db)


@router.get("/{id}", status_code = status.HTTP_200_OK, response_model=UserBase)
async def get_user(
        id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    print('********* token **********', current_user.access_token)
    return await UserService.get_user(db=db, id=id)


@router.patch("/update", status_code = status.HTTP_200_OK, response_model=UserBase)
async def update_user(
        user_form: UserEditForm = Depends(UserEditForm),
        db: AsyncSession = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
    ):
    
    if user_form.username is not None:
        current_user.username = user_form.username
    if user_form.email is not None:
        current_user.email = user_form.email

    db.add(current_user)
    await db.commit()  
    await db.refresh(current_user)

    return current_user


@router.delete("/delete_by_id/{id}", status_code = status.HTTP_200_OK,)
async def delete_user_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
    if current_user.is_admin == True:
        return await UserService.delete_user(db, id)
    else:
        raise HTTPException(status_code=400, detail="Permission deny")
    

@router.delete("/delete_user_by_himself", status_code = status.HTTP_200_OK,)
async def delete_user_by_himself(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserBase = Depends(get_current_user)
):
      
    await db.delete(current_user)
    await db.commit()
    await db.flush()
        
    return {"message": "Your account has been deleted successfully!"}