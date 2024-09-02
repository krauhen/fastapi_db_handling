import os

from fastapi import FastAPI
from db_exp.util.db_handler import *
from db_exp.api.v1.user import router as user_router
from db_exp.api.v1.image import router as image_router
from db_exp.api.v1.metadata import router as metadata_router
from dotenv import load_dotenv


load_dotenv()


app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(metadata_router, prefix="/metadata", tags=["metadata"])


@app.on_event("startup")
def startup():
    user, password = get_auth_db()
    global db_params
    db_params = DBParams(dbname="image_database", user=user, password=password)
    create_database(db_params)
    create_tables(db_params)


@app.on_event("shutdown")
def shutdown():
    pass
