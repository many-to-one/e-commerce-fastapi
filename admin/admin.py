from core.security import get_current_user, verify_password
from dotenv import load_dotenv
import os, re
from fastapi import Response, Depends
from schemas.users import UserBase
from sqladmin import Admin, ModelView
from db.database import async_engine, async_session, get_db
from models.models import Category, Product, User
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from sqlalchemy.future import select
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Load environment variables from the .env file
load_dotenv()

#This page will implement the authentication for your admin pannel
class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username= form.get("username")
        password= form.get("password")
        session = async_session()
        result = await session.execute(select(User).filter(User.username == username))
        user = result.scalar_one_or_none()
        if verify_password(password, user.password):
            if user.is_admin:
                token = user.access_token
                if token:
                    request.session.update({"token": token})
                    return True
        else:
            False

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token is not None


# create a view for your models
class UsersAdmin(ModelView, model=User):
    column_list = [
        'id', 'email', 'username', 'is_admin'
    ]
    form_columns = {
        'id', 'email', 'username', 'is_admin', 'created_at'
    }

class CategoriesAdmin(ModelView, model=Category):
    column_list = [
        'id', 'name'
    ]
    form_columns = {
        'id', 'name'
    }

class ProductsAdmin(ModelView, model=Product):
    column_list = [
        'id', 'title'
    ]
    # form_columns = {
    #     'id', 'title'
    # }

# add the views to admin
def create_admin(app):
    authentication_backend = AdminAuth(secret_key=os.getenv("secret_key"))
    admin = Admin(app=app, engine=async_engine, authentication_backend=authentication_backend)
    admin.add_view(UsersAdmin)
    admin.add_view(CategoriesAdmin)
    admin.add_view(ProductsAdmin)
    
    return admin