from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from typing import List
import time

from contextlib import asynccontextmanager
import asyncio

from app.metrics import REQUEST_COUNT, metrics
from app.logger import logger
from app.config import APP_NAME, APP_VERSION, ENVIRONMENT

app_state = {
    "ready": False,
    "shutdown": False
}

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting CloudPulse...")

    # Simulate startup work
    await asyncio.sleep(2)

    app_state["ready"] = True

    logger.info("CloudPulse Ready")

    yield

    logger.info("Gracefully shutting down...")

    app_state["ready"] = False
    app_state["shutdown"] = True

    await asyncio.sleep(2)

    logger.info("Shutdown Complete")


app = FastAPI(
    title=APP_NAME,
    description="Enterprise DevOps Demo API",
    version=APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    id: int
    name: str
    email: str


users: List[User] = []


@app.get("/")
def home():

    REQUEST_COUNT.inc()

    return {

        "application": APP_NAME,

        "version": APP_VERSION,

        "status": "Running",

        "environment": ENVIRONMENT
    }

@app.get("/ready")
def ready():

    REQUEST_COUNT.inc()

    if app_state["ready"]:

        return {
            "status": "Ready"
        }

    raise HTTPException(
        status_code=503,
        detail="Application not ready"
    )

@app.get("/health")
def health():

    REQUEST_COUNT.inc()

    return {

        "status": "Healthy",

        "application": APP_NAME,

        "version": APP_VERSION,

        "shutdown": app_state["shutdown"]

    }


@app.get("/version")
def version():

    REQUEST_COUNT.inc()

    return {

        "application": APP_NAME,

        "version": APP_VERSION

    }


@app.get("/users", response_model=List[User])
def get_users():
    REQUEST_COUNT.inc()

    return users


@app.post("/users", status_code=201)
def create_user(user: User):

    REQUEST_COUNT.inc()

    for u in users:
        if u.id == user.id:
            raise HTTPException(
                status_code=400,
                detail="User ID already exists"
            )

    users.append(user)

    logger.info(
    f"Created User ID={user.id} NAME={user.name}"
)

    return {
        "message": "User Added",
        "user": user
    }

@app.get("/metrics")
def get_metrics():
    return metrics()


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Time={duration:.4f}s"
    )

    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.error(str(exc))

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )
