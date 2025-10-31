from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 🔹 Base común
class UserBase(BaseModel):
    nombre: str
    apellidos: str
    email: str
    hashed_password: str
    role_id: int  # 🔹 Nuevo campo obligatorio


# 🔹 Crear usuario
class UserCreate(UserBase):
    pass


# 🔹 Obtener usuario por ID
class UserGet(BaseModel):
    id: int


# 🔹 Actualizar usuario
class UserUpdate(BaseModel):
    id: int
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    role_id: Optional[int] = None  # 🔹 Se puede cambiar el rol


# 🔹 Eliminar usuario
class UserDelete(BaseModel):
    id: int


# 🔹 Leer usuario desde la DB
class UserRead(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: str
    role_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
