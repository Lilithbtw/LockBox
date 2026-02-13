from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.requests import Request
from sqlalchemy import select, delete

from ..auth import verify_password, get_user_by_username, hash_password
from ..database import AsyncSessionLocal
from ..models import *

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

async def homepage(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    async with AsyncSessionLocal() as session:
        stmt = select(To_Do).where(To_Do.user_id == user_id)
        result = await session.execute(stmt)
        user_tasks = result.scalars().all()
        
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "tasks": user_tasks,
        }
    )

async def not_found(request: Request, exc: HTTPException):
    print(request.url)
    return templates.TemplateResponse("notfound.html",
                                        {"request": request},
                                        status_code=exc.status_code
                                    )

async def login_page(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html",{"request": request, "error":error})

async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html",{"request": request})


async def add_task(request: Request):
    current_id = request.session.get("user_id")

    if not current_id:
        return RedirectResponse(url="/login",status_code=303)

    form = await request.form()
    task = form.get("task")

    if task:
        async with AsyncSessionLocal() as session:
            entry = To_Do(
                task=task,
                user_id=current_id
            )
            session.add(entry)
            await session.commit()

    return RedirectResponse("/", status_code=303)

async def delete_task(request: Request):
    # 'index' here is actually the task's database ID
    task_id = int(request.path_params["index"])
    current_user_id = request.session.get("user_id")

    if not current_user_id:
        return RedirectResponse(url="/login", status_code=303)

    async with AsyncSessionLocal() as session:
        # We filter by task_id AND user_id so users can't delete each other's tasks
        stmt = delete(To_Do).where(
            To_Do.id == task_id, 
            To_Do.user_id == current_user_id
        )
        await session.execute(stmt)
        await session.commit()

    return RedirectResponse("/", status_code=303)
async def signup(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    
    if not username or not password:
        return RedirectResponse(url="/signup", status_code=303)
    
    hashed = hash_password(password)
    
    async with AsyncSessionLocal() as session:
        new_user = User(username=username, password_hash=hashed)
        session.add(new_user)
        try:
            await session.commit()
        except Exception as e:
            print(f"Error creating user: {e}")
            return RedirectResponse(url="/signup", status_code=303)
        
    return RedirectResponse(url="/login", status_code=303)

async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    async with AsyncSessionLocal() as session:
        user = await get_user_by_username(session, username)
        if user and verify_password(password, user.password_hash):
            request.session["user_id"] = user.id
            return RedirectResponse(url="/", status_code=303)

    return RedirectResponse(url="/login?error=Invalid+credentials", status_code=303)

async def logout(request: Request):
    request.session.clear() # Deletes the session cookie
    return RedirectResponse(url="/login", status_code=303)