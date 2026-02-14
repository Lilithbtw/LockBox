from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.requests import Request
from sqlalchemy import select, delete
from pydantic import BaseModel

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
        items = result.scalars().all()
        
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "items": items,
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

class VaultEntry(BaseModel):
    name: str | None = None
    domain: str
    domain_usr: str
    domain_pass: str

async def add_task(request: Request):
    current_id = request.session.get("user_id")

    if not current_id:
        return RedirectResponse(url="/login", status_code=303)

    try:
        data = await request.json()
        entry_data = VaultEntry(**data)
    except Exception as e:
        print(f"Invalid JSON or missing fields: {e}")
        return HTMLResponse(content="Bad Request", status_code=400)

    async with AsyncSessionLocal() as session:
        new_entry = To_Do(
            user_id=current_id,
            name=entry_data.name,
            domain=entry_data.domain,
            domain_usr=entry_data.domain_usr,
            domain_pass=entry_data.domain_pass
        )
        session.add(new_entry)
        await session.commit()
    
    # 3. Return a JSON success response (Fetch expects this)
    return HTMLResponse(content="Success", status_code=200)

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

async def edit(request: Request):
    task_id = int(request.path_params["index"])
    current_user_id = request.session.get("user_id")

    if not current_user_id:
        return HTMLResponse(content="Unauthorized", status_code=401)

    try:
        data = await request.json()
        entry_data = VaultEntry(**data)
    except Exception as e:
        return HTMLResponse(content="Invalid Data", status_code=400)

    async with AsyncSessionLocal() as session:
        # Security: Ensure the task belongs to the user logged in
        stmt = select(To_Do).where(To_Do.id == task_id, To_Do.user_id == current_user_id)
        result = await session.execute(stmt)
        db_item = result.scalar_one_or_none()

        if not db_item:
            return HTMLResponse(content="Not Found", status_code=404)

        db_item.domain = entry_data.domain
        db_item.domain_usr = entry_data.domain_usr
        db_item.domain_pass = entry_data.domain_pass

        await session.commit()
    
    return HTMLResponse(content="Updated", status_code=200)
    
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
            await session.refresh(new_user) # Get the new ID
            
            # Log them in immediately so the sessionStorage key stays valid
            request.session["user_id"] = new_user.id 
            return RedirectResponse(url="/", status_code=303)
            
        except Exception as e:
            print(f"Error: {e}")
            return RedirectResponse(url="/signup", status_code=303)

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