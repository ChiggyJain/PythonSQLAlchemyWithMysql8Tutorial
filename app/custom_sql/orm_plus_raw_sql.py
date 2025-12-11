import asyncio
from sqlalchemy import text, select
from app.db.database import AsyncSessionLocal
from app.db.models import AsyncUser


async def raw_to_orm():
    async with AsyncSessionLocal() as session:
        stmt = select(AsyncUser).from_statement(
            text("SELECT id, name FROM async_users WHERE name LIKE :name")
        )
        result = await session.execute(stmt, {"name": "%u"})
        users = result.scalars().all()
        print("\nORM Objects Returned From RAW SQL:")
        for u in users:
            print(u.id, u.name)


if __name__ == "__main__":
    asyncio.run(raw_to_orm())
