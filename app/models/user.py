from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    role = relationship("Role")
    posts = relationship("Post", back_populates="owner", lazy="selectin")

    # 🔹 Query personalizado para filtrar activos
    @classmethod
    async def get_all_active(cls, db: AsyncSession):
        result = await db.execute(select(cls).where(cls.deleted_at.is_(None)))
        return result.scalars().all()

    @classmethod
    async def get_by_id_active(cls, db: AsyncSession, user_id: int):
        result = await db.execute(
            select(cls).where(cls.id == user_id, cls.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()
