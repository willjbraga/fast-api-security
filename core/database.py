from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = async_sessionmaker(
    engine,
    class_ =  AsyncSession,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False,
    bind = engine
)