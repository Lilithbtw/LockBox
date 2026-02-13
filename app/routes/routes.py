from starlette.routing import Route
from starlette.responses import FileResponse, JSONResponse

from .views import *

routes = [
    Route("/", homepage),
    Route("/add", add_task, methods=["POST"]),
    Route("/delete/{index:int}", delete_task),
 
    Route("/login", login_page, methods=["GET"]),
    Route("/login", login, methods=["POST"]),
    
    Route("/signup", signup_page, methods=["GET"]),
    Route("/signup", signup, methods=["POST"]),

    Route("/logout", logout),

    Route("/favicon.ico", lambda r: FileResponse('app/static/favicon.ico')),
    Route("/health", lambda r: JSONResponse({'Health': 'Ok'}))
]
