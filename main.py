from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
# from sqladmin import Admin
from admin.admin import create_admin

from redis_.redisA import RedisClient
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from routers import auth, carts, users, categories, products

from redis import Redis
import httpx

app = FastAPI()

origins = [
    "http://localhost:3000",  # React app running locally
    # Add other origins as needed
]

# Add CORS middleware to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

admin = create_admin(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(carts.router)



client = RedisClient(host='redis', port=6379)

@app.get("/set-redis/")
async def set_redis_value():
    # Set a key-value pair in Redis
    await client.set_value("test_key", "test_value")
    return {"message": "Value set in Redis"}

@app.get("/get-redis/")
async def get_redis_value():
    # Get a value from Redis
    value = await client.get_value("test_key")
    return {"message": f"Value from Redis: {value.decode('utf-8')}"}


@app.get("/")
async def root():
    return {'message': 'Hello World!'}