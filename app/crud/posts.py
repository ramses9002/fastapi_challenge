from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostDelete
from app.utils.response_helper import response_success, response_error
from app.utils.security import check_permission

class PostCRUD:
    async def create(self, db: AsyncSession, post: PostCreate):
        try:
            # 🔹 Verificar si el usuario propietario existe
            owner = await User.get_by_id_active(db, post.owner_id)
            if not owner:
                return response_error(message="El usuario propietario no existe o fue eliminado")

            new_post = Post(**post.model_dump())
            db.add(new_post)
            await db.commit()
            await db.refresh(new_post)
            return response_success(message="Post creado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al crear post: {e}")



    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        try:
            # 🔹 Usamos el método de clase que filtra deleted_at
            posts_active = await Post.get_all_active(db)
            total = len(posts_active)

            # 🔹 Paginación manual
            paginated_posts = posts_active[skip : skip + limit]

            # 🔹 Formatear la respuesta con datos del usuario
            data = [
                {
                    "id": p.id,
                    "title": p.title,
                    "content": p.content,
                    "owner": {
                        "id": p.owner.id,
                        "nombre": p.owner.nombre,
                        "apellidos": p.owner.apellidos,
                        "email": p.owner.email,
                    },
                    "created_at": p.created_at,
                    "updated_at": p.updated_at,
                }
                for p in paginated_posts
            ]

            return response_success(
                data={
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                    "posts": data
                }
            )
        except Exception as e:
            return response_error(message=f"Error al obtener posts: {e}")



    async def get_by_id(self, db: AsyncSession, post_id: int):
        try:
            db_post = await Post.get_by_id_active(db, post_id)
            if not db_post:
                return response_error(message="Post no encontrado")

            data = {
                "id": db_post.id,
                "title": db_post.title,
                "content": db_post.content,
                "owner_id": db_post.owner_id,
                "created_at": db_post.created_at,
                "updated_at": db_post.updated_at
            }
            return response_success(data=data)
        except Exception as e:
            return response_error(message=f"Error al buscar post: {e}")



    async def update(self, db: AsyncSession, post: PostUpdate, current_user):
        try:            
            db_post = await Post.get_by_id_active(db, post.id)
            if not db_post:
                return response_error(message="Post no encontrado")
            
            if not check_permission(current_user, "edit_post", db_post):
                return response_error(message="No tienes permiso para editar este post")
            
            update_data = post.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_post, key, value)

            await db.commit()
            await db.refresh(db_post)
            return response_success(message="Post actualizado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al actualizar post: {e}")



    async def delete(self, db: AsyncSession, post: PostDelete, current_user):
        try:
            db_post = await Post.get_by_id_active(db, post.id)
            if not db_post:
                return response_error(message="Post no encontrado")
            
            if not check_permission(current_user, "delete_post", db_post):
                return response_error(message="No tienes permiso para eliminar este post")
            
            db_post.deleted_at = datetime.utcnow()
            await db.commit()
            return response_success(message="Post eliminado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al eliminar post: {e}")


# 🔹 Instancia global para importar en routers
post_crud = PostCRUD()
