from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Code that runs before the request reaches the route handler
        print("Before request:", request.url)
        
        # Call the next middleware or route handler
        response = await call_next(request)
        
        # Code that runs after the route handler has processed the request
        print("After response:", response.status_code)
        
        return response
    
class RouterSpecificMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the request path is from the specific router
        if request.url.path.startswith("/items"):
            print("Middleware applied to /items path")
        else:
            print("Middleware skipped")

        # Call the next middleware or route handler
        response = await call_next(request)
        return response