from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware


middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=['localhost']),
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9),
    Middleware(SessionMiddleware, secret_key="SUPER_SECRET_STRING"),
]
