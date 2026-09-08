from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.configs import settings

# Essa parte  configura exatamente o pool de conexões que se refere a quantas conexões simultaneas são possíves
# Autalmente o máximo de conexão ao mesmo tempo é pool_size + max_overflow (10 + 20)
engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
)

Session = async_sessionmaker(
    bind = engine,
    #class_ =  AsyncSession, -> async_sessionmaker já usar AsynccSession por padrão
    #autocommit = False, -> no modelo novo usa transações explicitas e não necessta de autocimmit
    #autoflush = False, -> é recomendavel deixar true como padrão
    expire_on_commit = False,
)