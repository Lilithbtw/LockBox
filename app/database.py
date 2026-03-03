from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from os import getenv
from dotenv import load_dotenv
import asyncio

load_dotenv()

USER = getenv("DB_USER")
PASSWORD = getenv("DB_PASS")
PORT = getenv("DB_PORT", 3306)
DB_NAME = getenv("DB_NAME")
HOST = getenv("DB_HOST")

SERVER_URL = f"mysql+asyncmy://{USER}:{PASSWORD}@{HOST}:{PORT}"
DATABASE_URL = f"{SERVER_URL}/{DB_NAME}"

async def create_db_if_not_exists():
    temp_engine = create_async_engine(SERVER_URL)
    retries = 10
    while retries > 0:
        try:
            async with temp_engine.connect() as conn:
                await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
                await conn.commit()
            await temp_engine.dispose()
        except (OperationalError,Exception) as e:
            retries -= 1
            print(f"Database not ready... waiting. Retries left: {retries} (Error: {e}")
            if retries == 0:
                raise e
            await asyncio.sleep(3)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()