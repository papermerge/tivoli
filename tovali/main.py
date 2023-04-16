import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer()

SECRET_KEY = os.environ['PAPERMERGE__SECURITY__SECRET_KEY']
ALGORITHM = os.environ['PAPERMERGE__SECURITY__TOKEN_ALGORITHM']


@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]) -> None:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
