from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models.user import User


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).order_by(User.name.desc()).limit(20))
    return result.scalars().all()


def add_users(session: AsyncSession, name: str):
    new_city = User(name=name)
    session.add(new_city)
    return new_city
