from starlette.applications import Starlette

from routes import routes
from middleware import middleware
from views import not_found

app = Starlette(debug=True, routes=routes, middleware=middleware)

app.add_exception_handler(404, not_found)