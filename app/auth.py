from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from argon2 import PasswordHasher, exceptions

from .models import *

ph = PasswordHasher()
def hash_password(password: str) -> str:
    return ph.hash(password)

async def get_user_by_username(session: AsyncSession, username: str):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalars().first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except exceptions.VerifyMismatchError:
        return False