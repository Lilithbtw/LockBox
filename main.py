from starlette.applications import Starlette
from starlette.responses import RedirectResponse, FileResponse, HTMLResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware

# Store tasks in-memory
tasks = []

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")


async def homepage(request: Request):
    return templates.TemplateResponse("index.html", 
                                            {
                                            "request": request,
                                            "tasks": list(enumerate(tasks)),
                                            "name": "Marshmallow :3"
                                            }
                                    )


async def add_task(request: Request):
    form = await request.form()
    task = form.get("task")
    print(form)
    print(task)
    if task:
        tasks.append(task)
    return RedirectResponse("/", status_code=303)


async def delete_task(request: Request):
    index = int(request.path_params["index"])
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return RedirectResponse("/", status_code=303)

async def not_found(request: Request, exc: HTTPException):
    print(request)
    return templates.TemplateResponse("notfound.html",
                                        {
                                        "request": request
                                        },
                                    status_code=exc.status_code
                                    )
routes = [
    Route("/", homepage),
    Route("/add", add_task, methods=["POST"]),
    Route("/delete/{index:int}", delete_task),
    Route("/favicon.ico", FileResponse('src/favicon.ico'))
]

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=['localhost']),
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)
]

exception_handlers = {
    404: not_found
}

app = Starlette(debug=True, routes=routes, middleware=middleware, exception_handlers=exception_handlers)