from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 🔹 Base común para los modelos de Post
class PostBase(BaseModel):
    title: str
    content: str
    owner_id: int


# 🔹 Crear Post
class PostCreate(PostBase):
    pass


# 🔹 Obtener Post por ID (usado en body)
class PostGet(BaseModel):
    id: int


# 🔹 Actualizar Post
class PostUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None


# 🔹 Eliminar Post (soft delete)
class PostDelete(BaseModel):
    id: int


# 🔹 Leer Post desde DB (respuesta)
class PostRead(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite leer desde objetos ORM de SQLAlchemy
