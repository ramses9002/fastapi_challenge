from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserDelete, UserGet
from app.crud.users import user_crud
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/create")
async def create_user_endpoint(user: UserCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await user_crud.create(db, user)


@router.get("/all")
async def get_all_users_endpoint(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros a traer"),
    db: AsyncSession = Depends(get_db),
    current_user= Depends(get_current_user)
):
    """
    Obtiene todos los usuarios activos con paginación.
    """
    return await user_crud.get_all(db, skip=skip, limit=limit)


@router.post("/get")
async def get_user_by_id_endpoint(user_data: UserGet, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await user_crud.get_by_id(db, user_data.id)


@router.post("/update")
async def update_user_endpoint(user_data: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await user_crud.update(db, user_data)


@router.post("/delete")
async def delete_user_endpoint(user_data: UserDelete, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await user_crud.delete(db, user_data)
