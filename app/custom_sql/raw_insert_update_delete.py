import asyncio
from sqlalchemy import text
from app.db.database import AsyncSessionLocal


async def raw_insert():
    async with AsyncSessionLocal() as session:
        sql = text("""
            INSERT INTO async_users (name, email)
            VALUES (:name, :email)
        """)
        await session.execute(sql, {
            "name": "RawSQL User",
            "email": "raw@example.com"
        })
        await session.commit()
        print("INSERT DONE")


async def raw_update():
    async with AsyncSessionLocal() as session:
        sql = text("""
            UPDATE async_users
            SET name = :name
            WHERE id = :id
        """)
        await session.execute(sql, {"id": 1, "name": "Updated via RAW SQL"})
        await session.commit()
        print("UPDATE DONE")


async def raw_delete():
    async with AsyncSessionLocal() as session:
        sql = text("DELETE FROM async_users WHERE id = :id")
        await session.execute(sql, {"id": 2})
        await session.commit()
        print("DELETE DONE")


async def main():
    await raw_insert()
    await raw_update()
    await raw_delete()


if __name__ == "__main__":
    asyncio.run(main())
