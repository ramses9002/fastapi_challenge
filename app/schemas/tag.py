from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 🔹 Base común para los modelos de Tag
class TagBase(BaseModel):
    name: str

# 🔹 Crear Tag
class TagCreate(TagBase):
    post_ids: List[int]  # IDs de posts a los que se asociará el tag

# 🔹 Obtener Tag por ID (usado en body)
class TagGet(BaseModel):
    id: int

# 🔹 Actualizar Tag
class TagUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    post_ids: Optional[List[int]] = None  # Lista de posts a asociar, opcional

# 🔹 Eliminar Tag (soft delete)
class TagDelete(BaseModel):
    id: int

# 🔹 Leer Tag desde DB (respuesta)
class TagRead(TagBase):
    id: int
    posts: List[dict]  # Cada post tendrá id, title, content y owner
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite leer desde objetos ORM de SQLAlchemy
