from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
import secrets
import os
from dotenv import load_dotenv

load_dotenv("../.env")

SESSION_SECRET = secrets.token_urlsafe(32)

middleware = [
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9),
    Middleware(SessionMiddleware, secret_key=SESSION_SECRET),
]

ALLOWED_HOSTS_STR = os.getenv("ALLOWED_HOSTS", "any")

if ALLOWED_HOSTS_STR.lower() != "any":
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(",") if host.strip()]
    middleware.append(Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS))