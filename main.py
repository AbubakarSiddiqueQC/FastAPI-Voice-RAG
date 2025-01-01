from contextlib import asynccontextmanager
from src.middlewares import AuthMiddleware
from src.apis import apis
from src.prisma import prisma
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await prisma.connect()
    yield  # Application runs while the context manager is active
    # Shutdown logic
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=1000)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

exempt_routes = [
    "/",
    "/favicon.ico",
    "/apis/public",
    "/apis/auth/login",
    "/apis/department/getDeparment",
    "/apis/department/addDeparment"
    ]
# app.add_middleware(AuthMiddleware, exempt_routes=exempt_routes)

app.include_router(apis, prefix="/apis")


@app.get("/")
def read_root():
    return {"version": "1.0.0"}
