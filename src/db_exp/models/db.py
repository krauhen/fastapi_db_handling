from typing import Optional
from pydantic import BaseModel


class DBParams(BaseModel):
    dbname: str
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
