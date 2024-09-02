from fastapi import APIRouter, HTTPException, Depends, Query
from db_exp.util.db_handler import get_db
from db_exp.models.db import Image


router = APIRouter()


@router.post("/", response_model=Image)
async def create_image(image: Image, conn=Depends(get_db)):
    query = """INSERT INTO images (user_id, image_url) VALUES ($1, $2) RETURNING image_id, user_id, image_url, upload_date"""
    result = await conn.fetchrow(query, image.user_id, image.image_url)
    if not result:
        raise HTTPException(status_code=400, detail="Image creation failed")
    return Image(**result)


@router.get("/{image_id}", response_model=Image)
async def get_image(image_id: int, conn=Depends(get_db)):
    query = """SELECT image_id, user_id, image_url, upload_date FROM images WHERE image_id = $1"""
    result = await conn.fetchrow(query, image_id)
    if not result:
        raise HTTPException(status_code=404, detail="Image not found")
    return Image(**result)


@router.put("/{image_id}", response_model=Image)
async def update_image(image_id: int, image: Image, conn=Depends(get_db)):
    query = """UPDATE images SET user_id = $1, image_url = $2 WHERE image_id = $3 RETURNING image_id, user_id, image_url, upload_date"""
    result = await conn.fetchrow(query, image.user_id, image.image_url, image_id)
    if not result:
        raise HTTPException(status_code=404, detail="Image not found")
    return Image(**result)


@router.delete("/{image_id}")
async def delete_image(image_id: int, conn=Depends(get_db)):
    query = """DELETE FROM images WHERE image_id = $1"""
    result = await conn.execute(query, image_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}
