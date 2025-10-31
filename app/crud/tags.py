from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.tag import Tag
from app.models.post import Post
from app.schemas.tag import TagCreate, TagUpdate, TagDelete
from app.utils.response_helper import response_success, response_error


class TagCRUD:

    # 🔹 Crear tag con posts activos
    async def create(self, db: AsyncSession, tag: TagCreate):
        try:
            # Validar y obtener posts activos
            posts = []
            for post_id in tag.post_ids:
                db_post = await Post.get_by_id_active(db, post_id)
                if not db_post:
                    return response_error(message=f"El post con ID {post_id} no existe o está eliminado")
                posts.append(db_post)

            new_tag = Tag(name=tag.name)
            new_tag.posts = posts

            db.add(new_tag)
            await db.commit()
            await db.refresh(new_tag)
            return response_success(message="Tag creado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al crear tag: {e}")

    # 🔹 Obtener todos los tags activos
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10):
        try:
            tags_active = await Tag.get_all_active(db)
            total = len(tags_active)
            paginated_tags = tags_active[skip: skip + limit]

            data = []
            for t in paginated_tags:
                data.append({
                    "id": t.id,
                    "name": t.name,
                    "posts": [
                        {
                            "id": p.id,
                            "title": p.title,
                            "content": p.content,
                            "owner": {
                                "id": p.owner.id,
                                "nombre": p.owner.nombre,
                                "apellidos": p.owner.apellidos,
                                "email": p.owner.email
                            }
                        } for p in t.posts
                    ],
                    "created_at": t.created_at,
                    "updated_at": t.updated_at
                })

            return response_success(
                data={
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                    "tags": data
                }
            )
        except Exception as e:
            return response_error(message=f"Error al obtener tags: {e}")

    # 🔹 Obtener tag activo por ID
    async def get_by_id(self, db: AsyncSession, tag_id: int):
        try:
            db_tag = await Tag.get_by_id_active(db, tag_id)
            if not db_tag:
                return response_error(message="Tag no encontrado")

            data = {
                "id": db_tag.id,
                "name": db_tag.name,
                "posts": [
                    {
                        "id": p.id,
                        "title": p.title,
                        "content": p.content,
                        "owner": {
                            "id": p.owner.id,
                            "nombre": p.owner.nombre,
                            "apellidos": p.owner.apellidos,
                            "email": p.owner.email
                        }
                    } for p in db_tag.posts
                ],
                "created_at": db_tag.created_at,
                "updated_at": db_tag.updated_at
            }
            return response_success(data=data)
        except Exception as e:
            return response_error(message=f"Error al buscar tag: {e}")

    # 🔹 Actualizar tag y posts
    async def update(self, db: AsyncSession, tag: TagUpdate):
        try:
            db_tag = await Tag.get_by_id_active(db, tag.id)
            if not db_tag:
                return response_error(message="Tag no encontrado")

            update_data = tag.model_dump(exclude_unset=True)

            if "name" in update_data:
                db_tag.name = update_data["name"]

            if "post_ids" in update_data:
                if update_data["post_ids"]:
                    posts = []
                    for post_id in update_data["post_ids"]:
                        db_post = await Post.get_by_id_active(db, post_id)
                        if not db_post:
                            return response_error(message=f"El post con ID {post_id} no existe o está eliminado")
                        posts.append(db_post)
                    db_tag.posts = posts
                else:
                    db_tag.posts = []

            await db.commit()
            await db.refresh(db_tag)
            return response_success(message="Tag actualizado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al actualizar tag: {e}")

    # 🔹 Soft delete
    async def delete(self, db: AsyncSession, tag: TagDelete):
        try:
            db_tag = await Tag.get_by_id_active(db, tag.id)
            if not db_tag:
                return response_error(message="Tag no encontrado")

            db_tag.deleted_at = datetime.utcnow()
            await db.commit()
            return response_success(message="Tag eliminado correctamente")
        except Exception as e:
            await db.rollback()
            return response_error(message=f"Error al eliminar tag: {e}")


# 🔹 Instancia global
tag_crud = TagCRUD()
