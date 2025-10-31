# app/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear motor async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # True para ver las queries en consola, útil en desarrollo
    future=True
)

# Crear sesión async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependencia para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
