from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin, SoftDeleteMixin
from app.models.post_tag import post_tag_table
from sqlalchemy.future import select

class Tag(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    posts = relationship("Post", secondary=post_tag_table, back_populates="tags", lazy="selectin")

    # 🔹 Obtener todos los tags activos
    @classmethod
    async def get_all_active(cls, db):
        result = await db.execute(cls.get_select_all_active())
        return result.scalars().all()

    # 🔹 Obtener tag activo por ID
    @classmethod
    async def get_by_id_active(cls, db, tag_id: int):
        result = await db.execute(cls.get_select_by_id_active(tag_id))
        return result.scalar_one_or_none()

    # 🔹 Consultas auxiliares para select
    @classmethod
    def get_select_all_active(cls):
        return select(cls).where(cls.deleted_at.is_(None))

    @classmethod
    def get_select_by_id_active(cls, tag_id: int):
        return select(cls).where(cls.id == tag_id, cls.deleted_at.is_(None))
