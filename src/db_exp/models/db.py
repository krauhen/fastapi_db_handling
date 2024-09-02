from typing import Optional
from pydantic import BaseModel


class Auth(BaseModel):
    user: str
    password: str


class DBParams(BaseModel):
    dbname: str = "postgres"
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432


class User(BaseModel):
    user_id: Optional[int]
    username: str
    email: str


class Image(BaseModel):
    image_id: Optional[int]
    user_id: int
    image_url: str
    upload_date: Optional[str]


class Metadata(BaseModel):
    metadata_id: Optional[int]
    image_id: int
    key: str
    value: str
