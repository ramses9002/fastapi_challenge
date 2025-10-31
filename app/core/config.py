# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = "postgresql+asyncpg://postgres:9145@localhost:5432/challengefastapi"

    # JWT
    SECRET_KEY: str = "c9f1a7d2b4e8f6c3a1d9e7b5c2f8a0d6"  # clave segura generada aleatoriamente
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 1 días

    # Otros parámetros opcionales
    APP_NAME: str = "Challenge FastAPI"

settings = Settings()
