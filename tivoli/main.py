from jose import JWTError, jwt

from fastapi import Request, Response, FastAPI, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from .config import Settings


app = FastAPI()
settings = Settings()


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


@app.api_route(
    "/{whatever:path}",
    methods=["GET", "POST", "PATCH", "PUT", "OPTIONS", "DELETE"]
)
async def root(request: Request) -> Response:
    token = get_token(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        jwt.decode(
            token,
            settings.papermerge__security__secret_key,
            algorithms=[settings.papermerge__security__token_algorithm]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return Response(status_code=status.HTTP_200_OK)
