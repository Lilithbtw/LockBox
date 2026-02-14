from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="/home/lilith/projects/LockBox/.env")

USER = getenv("DB_USER")
PASSWORD = getenv("DB_PASS")
PORT = getenv("DB_PORT", 3306)
DB_NAME = getenv("DB_NAME")
HOST = getenv("DB_HOST")

SERVER_URL = f"mysql+asyncmy://{USER}:{PASSWORD}@{HOST}:{PORT}"

DATABASE_URL = f"{SERVER_URL}/{DB_NAME}"

async def create_db_if_not_exists():
    temp_engine = create_async_engine(SERVER_URL) 
    async with temp_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        await conn.commit() # We commit the changes to the DB
    await temp_engine.dispose()

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()