from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.post import PostCreate, PostUpdate, PostDelete, PostGet
from app.crud.posts import post_crud
from app.core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create")
async def create_post_endpoint(post: PostCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await post_crud.create(db, post)



@router.get("/all")
async def get_all_posts_endpoint(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a traer"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Obtiene todos los posts activos con paginación.
    """
    return await post_crud.get_all(db, skip=skip, limit=limit)



@router.post("/get")
async def get_post_by_id_endpoint(post_data: PostGet, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await post_crud.get_by_id(db, post_data.id)



@router.post("/update")
async def update_post_endpoint(post_data: PostUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await post_crud.update(db, post_data, current_user)



@router.post("/delete")
async def delete_post_endpoint(post_data: PostDelete, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await post_crud.delete(db, post_data, current_user)
