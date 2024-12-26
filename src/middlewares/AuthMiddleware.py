from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.auth import decodeJWT

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_routes=None):
        super().__init__(app)
        self.exempt_routes = exempt_routes or []

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for exempted routes
        if request.url.path in self.exempt_routes:
            return await call_next(request)

        # Check for Authorization header
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Decode the token
        token = token[7:]  # Remove "Bearer " prefix
        decoded = decodeJWT(token)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Attach user info to the request state
        request.state.user = decoded

        return await call_next(request)
