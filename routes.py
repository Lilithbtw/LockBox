from starlette.routing import Route
from starlette.responses import FileResponse, JSONResponse

from views import *

routes = [
    Route("/", homepage),
    Route("/add", add_task, methods=["POST"]),
    Route("/delete/{index:int}", delete_task),
    Route("/favicon.ico", FileResponse('src/favicon.ico')),
    Route("/health", JSONResponse({'Health': 'Ok'}))
]
