from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.role import Role

async def init_roles(db: AsyncSession):
    """Inserta los roles base si no existen."""
    default_roles = ["admin", "cant_edit", "cant_delete"]

    for role_name in default_roles:
        result = await db.execute(select(Role).where(Role.name == role_name))
        existing_role = result.scalar_one_or_none()
        if not existing_role:
            db.add(Role(name=role_name))

    await db.commit()
