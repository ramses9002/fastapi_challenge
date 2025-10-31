from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.tag import TagCreate, TagUpdate, TagDelete, TagGet
from app.crud.tags import tag_crud
from app.core.security import get_current_user

router = APIRouter(prefix="/tags", tags=["Tags"])

# 🔹 Crear tag
@router.post("/create")
async def create_tag_endpoint(tag_data: TagCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await tag_crud.create(db, tag_data)



# 🔹 Obtener todos los tags
@router.get("/all")
async def get_all_tags_endpoint(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a traer"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await tag_crud.get_all(db, skip=skip, limit=limit)



# 🔹 Obtener tag por ID
@router.post("/get")
async def get_tag_by_id_endpoint(tag_data: TagGet, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await tag_crud.get_by_id(db, tag_data.id)



# 🔹 Actualizar tag
@router.post("/update")
async def update_tag_endpoint(tag_data: TagUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await tag_crud.update(db, tag_data)



# 🔹 Eliminar tag (soft delete)
@router.post("/delete")
async def delete_tag_endpoint(tag_data: TagDelete, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await tag_crud.delete(db, tag_data)
