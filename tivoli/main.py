from jose import JWTError, jwt

from fastapi import Request, Response, FastAPI, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param

from .config import Settings


app = FastAPI()
settings = Settings()


@app.get("/")
async def root(request: Request) -> Response:
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
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
