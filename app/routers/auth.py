from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.auth import auth_crud
from app.db.session import get_db
from app.schemas.auth import AuthRegister, AuthLogin

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

@router.post("/register")
async def register_endpoint(user: AuthRegister, db: AsyncSession = Depends(get_db)):
    return await auth_crud.register(db, user)



@router.post("/login")
async def login_endpoint(user: AuthLogin, db: AsyncSession = Depends(get_db)):
    return await auth_crud.login(db, user)



@router.post("/refresh")
async def refresh_endpoint(token: str = Header(...)):
    return await auth_crud.refresh_token(token)
