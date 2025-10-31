from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserDelete
from app.utils.response_helper import response_success, response_error
from app.utils.security import hash_password


class UserCRUD:
    async def create(self, db: AsyncSession, user: UserCreate):
        try:
            # 🔹 Verificar si el correo ya existe
            result = await db.execute(select(User).where(User.email == user.email))
            existing_user = result.scalar_one_or_none()
            if existing_user:
                return response_error(message="El correo ya está registrado")

            # 🔹 Verificar que el rol exista
            role_result = await db.execute(select(Role).where(Role.id == user.role_id))
            role = role_result.scalar_one_or_none()
            if not role:
                return response_error(message="El rol especificado no existe")

            user_data = user.model_dump()
            # 🔹 Hashear la contraseña
            user_data["hashed_password"] = hash_password(user_data["hashed_password"])

            new_user = User(**user_data)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return response_success(message="Usuario creado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al crear usuario: {e}")



    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        try:
            # 🔹 Traer usuarios activos y cargar su role en la misma consulta
            result = await db.execute(
                select(User)
                .options(selectinload(User.role))
                .where(User.deleted_at.is_(None))
            )
            users_active = result.scalars().all()
            total = len(users_active)

            # 🔹 Paginación manual sobre la lista
            paginated_users = users_active[skip : skip + limit]

            # 🔹 Formateamos la respuesta incluyendo el nombre del role
            data = [
                {
                    "id": u.id,
                    "nombre": u.nombre,
                    "apellidos": u.apellidos,
                    "email": u.email,
                    "role": {
                        "id": u.role.id if u.role else None,
                        "name": u.role.name if u.role else None
                    },
                    "created_at": u.created_at,
                    "updated_at": u.updated_at
                } for u in paginated_users
            ]

            return response_success(
                data={
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                    "users": data
                }
            )
        except Exception as e:
            return response_error(message=f"Error al obtener usuarios: {e}")



    async def get_by_id(self, db: AsyncSession, user_id: int):
        try:
            # 🔹 Obtener usuario activo por id y cargar role
            result = await db.execute(
                select(User).options(selectinload(User.role)).where(User.id == user_id, User.deleted_at.is_(None))
            )
            db_user = result.scalar_one_or_none()
            if not db_user:
                return response_error(message="Usuario no encontrado")

            data = {
                "id": db_user.id,
                "nombre": db_user.nombre,
                "apellidos": db_user.apellidos,
                "email": db_user.email,
                "role": {
                    "id": db_user.role.id if db_user.role else None,
                    "name": db_user.role.name if db_user.role else None
                },
                "created_at": db_user.created_at,
                "updated_at": db_user.updated_at,
            }
            return response_success(data=data)
        except Exception as e:
            return response_error(message=f"Error al buscar usuario: {e}")



    async def update(self, db: AsyncSession, user: UserUpdate):
        try:
            db_user = await User.get_by_id_active(db, user.id)
            if not db_user:
                return response_error(message="Usuario no encontrado")

            update_data = user.model_dump(exclude_unset=True)

            # 🔹 Si viene contraseña, hashearla
            if "hashed_password" in update_data:
                update_data["hashed_password"] = hash_password(update_data["hashed_password"])

            # 🔹 Si viene role_id, validar que exista
            if "role_id" in update_data:
                role_result = await db.execute(select(Role).where(Role.id == update_data["role_id"]))
                if not role_result.scalar_one_or_none():
                    return response_error(message="El rol especificado no existe")

            if "email" in update_data:
                result_email = await db.execute(
                    select(User).where(
                        User.email == update_data["email"],
                        User.id != db_user.id,
                        User.deleted_at.is_(None),
                    )
                )
                existing_user = result_email.scalar_one_or_none()
                if existing_user:
                    return response_error(message="El correo ya está registrado por otro usuario")

            for key, value in update_data.items():
                setattr(db_user, key, value)

            await db.commit()
            await db.refresh(db_user)
            return response_success(message="Usuario actualizado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al actualizar usuario: {e}")



    async def delete(self, db: AsyncSession, user: UserDelete):
        try:
            db_user = await User.get_by_id_active(db, user.id)
            if not db_user:
                return response_error(message="Usuario no encontrado")

            # 🔹 Soft delete
            db_user.deleted_at = datetime.utcnow()
            await db.commit()
            return response_success(message="Usuario eliminado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al eliminar usuario: {e}")


# 🔹 Instancia global para importar en routers
user_crud = UserCRUD()
