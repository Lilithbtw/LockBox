from starlette.applications import Starlette
import os

from app.routes.routes import routes 
from app.middleware import middleware
from app.routes.views import * 
from app.database import engine, Base, create_db_if_not_exists

app = Starlette(debug=True, routes=routes, middleware=middleware)

app.add_exception_handler(404, not_found)

@app.on_event("startup")
async def startup():
    try:
        await create_db_if_not_exists()

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database and Tables initialized correctly!")
    except Exception as e:
        print(f"Failed to initialize Database Connection: {e}")
        os._exit(1)
