from fastapi import FastAPI

from contextlib import asynccontextmanager
from db_exp.util.azure_connector import get_secret, get_secret_client
from db_exp.util.db_handler import *
from db_exp.api.v1.user import router as user_router
from db_exp.api.v1.image import router as image_router
from db_exp.api.v1.metadata import router as metadata_router
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_secret_client()
        user = get_secret("user")
        password = get_secret("password")

        global db_params
        db_params = DBParams(database="image_database", user=user, password=password)

        await create_database(db_params)
        await create_tables(db_params)

        yield
    except Exception as e:
        raise e


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(metadata_router, prefix="/metadata", tags=["metadata"])
