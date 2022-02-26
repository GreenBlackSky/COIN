"""Backend initialization module."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from . import user
from . import account
from . import event
from . import category


app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = os.environ["JWT_SECRET_KEY"]


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(account.router)
app.include_router(event.router)
app.include_router(category.router)

# JWT_SECRET_KEY=os.environ["JWT_SECRET_KEY"],
# SECRET_KEY=os.environ["SECRET_KEY"],
# FLASK_ENV=os.environ["FLASK_ENV"],
# FLASK_APP=os.environ["FLASK_APP"],
# FLASK_DEBUG=os.environ["FLASK_DEBUG"],
# CORS_HEADERS="Content-Type",
