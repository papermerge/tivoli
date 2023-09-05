from jose import JWTError, jwt

from sqlalchemy.orm import Session
from fastapi import Depends, Request, Response, FastAPI, HTTPException, status

from database import get_db
from .config import Settings
from .utils import get_token, get_user

app = FastAPI()
settings = Settings()



@app.api_route(
    "/{whatever:path}",
    methods=["GET", "POST", "PATCH", "PUT", "OPTIONS", "DELETE"]
)
async def root(
    request: Request,
    db: Session = Depends(get_db)
) -> Response:
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

    # get_user(db, decoded_token['user_id'])

    return Response(status_code=status.HTTP_200_OK)
