from fastapi import APIRouter, HTTPException, Depends
from db_exp.util.db_handler import get_db
from db_exp.models.db import User


router = APIRouter()


@router.post("/", response_model=User)
async def create_user(user: User, conn=Depends(get_db)):
    query = """INSERT INTO users (username, email) VALUES ($1, $2) RETURNING user_id, username, email"""
    result = await conn.fetchrow(query, user.username, user.email)
    if not result:
        raise HTTPException(status_code=400, detail="User creation failed")
    return User(**result)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, conn=Depends(get_db)):
    query = """SELECT user_id, username, email FROM users WHERE user_id = $1"""
    result = await conn.fetchrow(query, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**result)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User, conn=Depends(get_db)):
    query = """UPDATE users SET username = $1, email = $2 WHERE user_id = $3 RETURNING user_id, username, email"""
    result = await conn.fetchrow(query, user.username, user.email, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**result)


@router.delete("/{user_id}")
async def delete_user(user_id: int, conn=Depends(get_db)):
    query = """DELETE FROM users WHERE user_id = $1"""
    result = await conn.execute(query, user_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
