from fastapi import APIRouter, HTTPException

from db_exp.models.v1 import user
from db_exp.models.v1.user import User, UserAlreadyExistsInDB, UserAdded, UserUpdated, UserDeleted
from psycopg import sql
from db_exp.util.database_manager import DatabaseManager
from typing import Union, List

router = APIRouter()


@router.post("/", response_model=Union[UserAdded, UserAlreadyExistsInDB])
async def create_user(user: User):
    try:
        with DatabaseManager().get_database_manager().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("SELECT user_id FROM users WHERE username = %s OR email = %s;"),
                    (user.username, user.email)
                )
                existing_user = cursor.fetchone()
                if existing_user:
                    return UserAlreadyExistsInDB(**user.dict())

                cursor.execute(
                    sql.SQL("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING user_id;"),
                    (user.username, user.email)
                )
                user_id = cursor.fetchone()[0]
                return {**user.dict(), "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    try:
        with DatabaseManager().get_database_manager().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("SELECT user_id, username, email FROM users WHERE user_id = %s;"),
                    (user_id,)
                )
                user = cursor.fetchone()
                if user is None:
                    raise HTTPException(status_code=404, detail="User not found.")
                return User(user_id=user[0], username=user[1], email=user[2])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=UserUpdated)
async def update_user(user_id: int, user: User):
    try:
        with DatabaseManager().get_database_manager().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("SELECT user_id FROM users WHERE user_id = %s;"),
                    (user_id,)
                )
                existing_user = cursor.fetchone()
                if existing_user is None:
                    raise HTTPException(status_code=404, detail="User not found.")

                cursor.execute(
                    sql.SQL("UPDATE users SET username = %s, email = %s WHERE user_id = %s;"),
                    (user.username, user.email, user_id)
                )

                return UserUpdated(**user.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", response_model=UserDeleted)
async def delete_user(user_id: int):
    try:
        with DatabaseManager().get_database_manager().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DELETE FROM users WHERE user_id = %s;"),
                    (user_id,)
                )
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="User not found.")

                return UserDeleted()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[User])
async def get_users():
    try:
        with DatabaseManager().get_database_manager().get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("SELECT user_id, username, email FROM users;"))
                users = cursor.fetchall()
                return [User(user_id=user[0], username=user[1], email=user[2]) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
