from uuid import UUID
from sqlalchemy.exc import OperationalError
from jose import JWTError, jwt
from sqlalchemy import Engine

from sqlalchemy.exc import NoResultFound
from fastapi import Depends, Request, Response, FastAPI, HTTPException, status

from .database import get_engine
from .config import Settings
from .utils import get_token, get_user

app = FastAPI()
settings = Settings()


@app.api_route(
    "/{whatever:path}",
    methods=["HEAD", "GET", "POST", "PATCH", "PUT", "OPTIONS", "DELETE"]
)
async def root(
    request: Request,
    engine: Engine = Depends(get_engine)
) -> Response:
    """
    Returns 200 OK response if and only if JWT token is valid

    JWT token is read either from authorization header or from
    cookie header. Token is considered valid if and only if both
    of the following conditions are true:
    - token was signed with PAPERMERGE__SECURITY__SECRET_KEY
    - User with user_id from the token is present in database
    """
    token = get_token(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        decoded_token = jwt.decode(
            token,
            settings.papermerge__security__secret_key,
            algorithms=[settings.papermerge__security__token_algorithm]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # token signature is valid: check

    if 'user_id' not in decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"user_id key not present in decoded token",
        )

    # token signature is valid: check
    # user_id key present in the token: check

    user_id = decoded_token['user_id']

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"user_id value is None",
        )

    # token signature is valid: check
    # user_id key present in the token: check
    # user_id value is not empty: check

    try:
        user = get_user(engine, UUID(user_id))
    except OperationalError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"DB operation error {exc}",
        )
    except NoResultFound:
        user = None

    # token signature is valid: check
    # user_id key present in the token: check
    # user_id value is not empty: check
    # database connection: check
    # database has core_user table: check

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with ID {user_id} not found in DB",
        )

    # token signature is valid: check
    # user_id key present in the token: check
    # user_id value is not empty: check
    # database connection: check
    # database has core_user table: check
    # user with given user_id present in core_user table: check
    return Response(status_code=status.HTTP_200_OK)
