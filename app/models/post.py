from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.base import Base, TimestampMixin, SoftDeleteMixin
from app.models.post_tag import post_tag_table

class Post(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="posts", lazy="selectin")
    tags = relationship("Tag", secondary=post_tag_table, back_populates="posts", lazy="selectin")

    
    # 🔹 Obtener todos los posts activos (sin deleted_at)
    @classmethod
    async def get_all_active(cls, db: AsyncSession):
        result = await db.execute(select(cls).where(cls.deleted_at.is_(None)))
        return result.scalars().all()

    # 🔹 Obtener un post activo por ID
    @classmethod
    async def get_by_id_active(cls, db: AsyncSession, post_id: int):
        result = await db.execute(
            select(cls).where(cls.id == post_id, cls.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()