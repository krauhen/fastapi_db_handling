import json

from fastapi import FastAPI
from contextlib import asynccontextmanager

from db_exp.api.v1.user import create_user
from db_exp.models.v1.user import User
from db_exp.api.v1.user import router as user_router
from db_exp.util.azure_connector import get_secret, get_secret_client
from db_exp.util.database_manager import DatabaseManager
from db_exp.models.db import *
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        get_secret_client()
        user = get_secret("user")
        password = get_secret("password")

        database = "image_database"
        db_params = DBParams(dbname=database, user=user, password=password)

        database_manager = DatabaseManager.get_database_manager()
        database_manager.set_db_default_params(db_params)
        database_manager.create_database(db_params.dbname)
        database_manager.create_table("user")

        with open("data/users.json") as f:
            users = json.load(f)
            for user in users:
                user = User(user_id=0, **user)
                await create_user(user)

        yield
    except Exception as e:
        raise e
    finally:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(user_router, prefix="/user", tags=["user"])
