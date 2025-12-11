
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select

# CHANGE THIS URL FOR YOUR MYSQL
DATABASE_URL = "mysql+asyncmy://c:Dharmilal%407186@localhost:3306/sqlalchemy_tutorial"


# -----------------------------------------------------------
# 1️⃣ ASYNC ENGINE
# -----------------------------------------------------------
engine = create_async_engine(DATABASE_URL, echo=True)


# -----------------------------------------------------------
# 2️⃣ ASYNC SESSION
# -----------------------------------------------------------
AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


# -----------------------------------------------------------
# 3️⃣ MODEL
# -----------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


# -----------------------------------------------------------
# 4️⃣ CREATE TABLES
# -----------------------------------------------------------
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# -----------------------------------------------------------
# 5️⃣ INSERT DATA
# -----------------------------------------------------------
async def create_user():
    async with AsyncSessionLocal() as session:
        user = User(name="Chirag")
        session.add(user)
        await session.commit()
        print("Inserted user")


# -----------------------------------------------------------
# 6️⃣ QUERY DATA
# -----------------------------------------------------------
async def fetch_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print("Users fetched:")
        for u in users:
            print(u.id, u.name)


# -----------------------------------------------------------
# MAIN RUNNER
# -----------------------------------------------------------
async def main():
    await init_db()
    await create_user()
    await fetch_users()


if __name__ == "__main__":
    asyncio.run(main())
