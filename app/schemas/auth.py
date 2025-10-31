from pydantic import BaseModel, EmailStr

# Para registro
class AuthRegister(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    password: str



# Para login
class AuthLogin(BaseModel):
    email: EmailStr
    password: str



# Para refrescar token
class TokenRefreshRequest(BaseModel):
    token: str
 

   
# Respuesta con JWT
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
