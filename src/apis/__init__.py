from fastapi import APIRouter

from src.apis.auth import router as authRouter
from src.apis.users import router as usersRouter
from src.apis.departmentApi import router as departmentRouter

apis = APIRouter()
apis.include_router(authRouter)
apis.include_router(usersRouter)
apis.include_router(departmentRouter)

__all__ = ["apis"]
