
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "mysql+asyncmy://c:Dharmilal%407186@localhost/sqlalchemy_tutorial"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async_Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            # provide session to API
            yield session
        finally:
            # always close session after completing the api request
            await session.close()