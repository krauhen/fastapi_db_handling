from fastapi import APIRouter, HTTPException, Depends, Query
from db_exp.util.db_handler import get_db
from db_exp.models.db import Metadata


router = APIRouter()


@router.post("/", response_model=Metadata)
async def create_metadata(metadata: Metadata, conn=Depends(get_db)):
    query = """INSERT INTO metadata (image_id, key, value) VALUES ($1, $2, $3) RETURNING metadata_id, image_id, key, value"""
    result = await conn.fetchrow(query, metadata.image_id, metadata.key, metadata.value)
    if not result:
        raise HTTPException(status_code=400, detail="Metadata creation failed")
    return Metadata(**result)


@router.get("/{metadata_id}", response_model=Metadata)
async def get_metadata(metadata_id: int, conn=Depends(get_db)):
    query = """SELECT metadata_id, image_id, key, value FROM metadata WHERE metadata_id = $1"""
    result = await conn.fetchrow(query, metadata_id)
    if not result:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return Metadata(**result)


@router.put("/{metadata_id}", response_model=Metadata)
async def update_metadata(metadata_id: int, metadata: Metadata, conn=Depends(get_db)):
    query = """UPDATE metadata SET image_id = $1, key = $2, value = $3 WHERE metadata_id = $4 RETURNING metadata_id, image_id, key, value"""
    result = await conn.fetchrow(
        query, metadata.image_id, metadata.key, metadata.value, metadata_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return Metadata(**result)


@router.delete("/{metadata_id}")
async def delete_metadata(metadata_id: int, conn=Depends(get_db)):
    query = """DELETE FROM metadata WHERE metadata_id = $1"""
    result = await conn.execute(query, metadata_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Metadata not found")
    return {"message": "Metadata deleted successfully"}
