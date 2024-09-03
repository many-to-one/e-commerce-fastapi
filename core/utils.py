# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.future import select
# from ..db.database import DATABASE_URL
# from ..models.models import Category

# async_engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )

# async def get_category_choices():
#     async with async_session() as session:
#         result = await session.execute(select(Category))
#         categories = result.scalars().all()
#         return [(category.id, category.name) for category in categories]