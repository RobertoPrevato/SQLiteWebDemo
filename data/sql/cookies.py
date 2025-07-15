from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from domain.cookies import Cookie, CookieRepository


class SQLiteCookieRepository(CookieRepository):
    """SQLite implementation of the CookieRepository."""

    session: AsyncSession

    async def pick_random(self) -> Cookie:
        """Pick a random cookie."""
        async with self.session as session:
            result = await session.execute(
                text("SELECT id, text FROM cookies ORDER BY RANDOM() LIMIT 1")
            )
            row = result.fetchone()
            if row:
                return Cookie(id=row[0], text=row[1])
            raise ValueError("No cookies found")  # or handle as needed
