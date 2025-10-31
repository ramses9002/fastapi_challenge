from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.auth import AuthRegister, AuthLogin
from app.utils.security import hash_password, verify_password
from app.core.security import create_access_token, decode_access_token
from app.utils.response_helper import response_success, response_error
from app.models.role import Role

class AuthCRUD:
    async def register(self, db: AsyncSession, user: AuthRegister):
        try:
            # 🔹 Verificar si el correo ya existe
            result = await db.execute(
                select(User).where(User.email == user.email, User.deleted_at.is_(None))
            )
            existing_user = result.scalar_one_or_none()
            if existing_user:
                return response_error(message="El correo ya está registrado")

            # 🔹 Obtener el rol por defecto (por ejemplo, "cant_edit")
            role_result = await db.execute(select(Role).where(Role.name == "admin"))
            role = role_result.scalar_one_or_none()
            if not role:
                return response_error(message="No se encontró el rol por defecto")

            # 🔹 Preparar datos del usuario
            user_data = user.model_dump()
            user_data["hashed_password"] = hash_password(user_data.pop("password"))
            user_data["role_id"] = role.id  # asigna el rol por defecto

            new_user = User(**user_data)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)

            # 🔹 Generar token JWT
            token = create_access_token(new_user.id)
            return response_success(
                data={"access_token": token, "token_type": "bearer"}
            )

        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al registrar usuario: {e}")


    async def login(self, db: AsyncSession, user: AuthLogin):
        try:
            result = await db.execute(
                select(User).where(User.email == user.email, User.deleted_at.is_(None))
            )
            db_user = result.scalar_one_or_none()
            if not db_user or not verify_password(user.password, db_user.hashed_password):
                return response_error(message="Credenciales incorrectas")

            token = create_access_token(db_user.id)
            return response_success(
                data={"access_token": token, "token_type": "bearer"}
            )
        except Exception as e:
            return response_error(message=f"Error en login: {e}")
        
    
    async def refresh_token(self, token: str):
        try:
            payload = decode_access_token(token)  # usa tu función existente
            user_id = payload.get("sub") if payload else None
            if not user_id:
                return response_error(message="Token inválido o expirado")

            new_token = create_access_token(user_id)
            return response_success(data={"access_token": new_token, "token_type": "bearer"})
        except Exception as e:
            return response_error(message=f"Error al refrescar token: {e}")

# Instancia global
auth_crud = AuthCRUD()
