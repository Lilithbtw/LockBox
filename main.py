from starlette.applications import Starlette
import os

from app.routes.routes import routes 
from app.middleware import middleware
from app.routes.views import * 
from app.database import engine, Base, create_db_if_not_exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import hash_password

app = Starlette(debug=True, routes=routes, middleware=middleware)

app.add_exception_handler(404, not_found)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.on_event("startup")
async def startup():
    try:
        await create_db_if_not_exists()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with async_session() as session:
            # Check if any users exist in the database
            result = await session.execute(select(func.count(User.id)))
            user_count = result.scalar()

            # Only proceed if the database is empty (count is 0)
            if user_count == 0:
                root_user = os.getenv("ROOT_USER")
                root_pass = os.getenv("ROOT_PASS")

                if root_user and root_pass:
                    new_root = User(
                        username=root_user,
                        password_hash=hash_password(root_pass)
                    )
                    session.add(new_root)
                    await session.commit()
                    print(f"Fresh database detected. Root user '{root_user}' created.")
                else:
                    print("Fresh database detected, but ROOT_USER or ROOT_PASS env vars are missing.")
            else:
                print(f"Database already initialized with {user_count} user(s). Skipping root creation.")
        
        print("Database and Tables initialized correctly!")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        os._exit(1)