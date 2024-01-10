from enum import Enum
from pydantic_settings import BaseSettings
from functools import lru_cache


class Algs(str, Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"


class Settings(BaseSettings):
    papermerge__security__secret_key: str
    papermerge__security__token_algorithm: Algs = Algs.HS256
    papermerge__security__cookie_name: str = 'access_token'

    # database where to read user table from
    papermerge__database__url: str = "sqlite:////db/db.sqlite3"


@lru_cache()
def get_settings():
    return Settings()
