
import asyncio
from sqlalchemy import text
from app.db.database import AsyncSessionLocal

async def raw_select_example():
    async with AsyncSessionLocal() as session:
        sql = text("""
            SELECT
            *
            FROM async_users
            WHERE 1 AND id>:id
            ORDER BY id DESC       
        """)
        result = await session.execute(sql, {'id': 0})
        rows = result.fetchall()
        print("\nPrint raw sql select result:")
        for r in rows:
            print(r.id, r.name, r.email)

if __name__ == "__main__":
    asyncio.run(raw_select_example())