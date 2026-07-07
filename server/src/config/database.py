from sqlalchemy.ext.asyncio import  create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo = True)

AsyncSesstionLocal = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

Base = declarative_base()

async def get_db():
    async with AsyncSesstionLocal() as session:
        yield session