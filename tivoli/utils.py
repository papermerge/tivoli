from uuid import UUID
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from fastapi import Request, FastAPI
from fastapi.security.utils import get_authorization_scheme_param

from .config import Settings
from . import models

app = FastAPI()
settings = Settings()


def get_user(engine: Engine, user_id: UUID) -> models.User:
    with Session(engine) as session:
        stmt = select(models.User).where(
            models.User.id == user_id
        )

        db_user = session.scalars(stmt).one()

    return db_user


def from_header(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        return None

    return token


def from_cookie(request: Request) -> str | None:
    cookie_name = settings.papermerge__security__cookie_name
    return request.cookies.get(cookie_name, None)


def get_token(request: Request) -> str | None:
    return from_cookie(request) or from_header(request)
