from passlib.context import CryptContext

# 🔹 Usamos Argon2 como esquema de hashing
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hashea la contraseña con Argon2"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica la contraseña ingresada contra el hash almacenado"""
    return pwd_context.verify(plain_password, hashed_password)


def check_permission(current_user, action: str, resource=None):
    role = current_user.role.name

    if resource and hasattr(resource, "owner_id"):
        if resource.owner_id == current_user.id:
            return True
            # if role == "admin":
            #     return True

            # if action == "edit_post" and role == "cant_edit":
            #     return True

            # if action == "delete_post" and role == "cant_delete":
            #     return True

    return False
