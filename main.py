from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from sqladmin import Admin
from admin.admin import create_admin

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from routers import auth, carts, users, categories, products


app = FastAPI()
admin = create_admin(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(carts.router)


@app.get("/")
async def root():
    return {'message': 'Hello World!'}