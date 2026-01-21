from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.requests import Request


# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Store tasks in-memory
tasks = []


async def homepage(request: Request):
    return templates.TemplateResponse("index.html", 
                                        {
                                            "request": request,
                                            "tasks": list(enumerate(tasks)),
                                            "name": "Marshmallow :3"
                                        }
                                    )


async def not_found(request: Request, exc: HTTPException):
    print(request.url)
    return templates.TemplateResponse("notfound.html",
                                        {"request": request},
                                        status_code=exc.status_code
                                    )

async def add_task(request: Request):
    form = await request.form()
    task = form.get("task")
    if task:
        tasks.append(task)
    return RedirectResponse("/", status_code=303)


async def delete_task(request: Request):
    index = int(request.path_params["index"])
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return RedirectResponse("/", status_code=303)

