from starlette.routing import Route
from starlette.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv

from .views import *

load_dotenv("../../.env")

onboarding = os.getenv("ONBOARDING")

routes = [
    Route("/", homepage),
    Route("/add", add_task, methods=["POST"]),
    Route("/delete/{index:int}", delete_task),
    
    Route("/login", login_page),
    Route("/login", login, methods=["POST"]),

    Route("/logout", logout),

    Route("/admin", admin_page),
    Route("/admin/delete-user/{user_id}", delete_user, methods=["POST"]),


    Route("/edit/{index:int}", edit, methods=["POST"]),

    Route("/favicon.ico", lambda r: FileResponse('app/static/favicon.png')),
    Route("/health", lambda r: JSONResponse({'Health': 'Ok'}))
]

if onboarding != None:
    routes.append(Route("/signup", signup, methods=["POST"]))
    routes.append(Route("/signup", signup_page))