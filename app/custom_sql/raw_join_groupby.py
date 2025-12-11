import asyncio
from sqlalchemy import text
from app.db.database import AsyncSessionLocal


async def user_post_report():
    async with AsyncSessionLocal() as session:
        sql = text("""
            SELECT 
            u.id,
            u.name,
            COUNT(p.id) AS total_posts
            FROM users u
            LEFT JOIN posts p ON p.user_id = u.id
            GROUP BY u.id
            HAVING total_posts >= :min_posts
            ORDER BY total_posts DESC
        """)
        result = await session.execute(sql, {"min_posts": 0})
        rows = result.fetchall()
        print("\nUSER POST REPORT:")
        for r in rows:
            print(r.name, r.total_posts)

if __name__ == '__main__':
    asyncio.run(user_post_report())
