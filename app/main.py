from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import users, auth, posts, tags
from app.core.middleware import TimerLoggingMiddleware
from app.db.session import get_db
from app.core.init_data import init_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa datos al iniciar la app (reemplaza on_event)."""
    async for db in get_db():
        await init_roles(db)  # Inserta roles por defecto si no existen
        break  # Evita dejar la sesión abierta
    yield 

app = FastAPI(
    title="Challenge FastAPI",
    description="API RESTful Challenge",
    version="1.0.0",
    lifespan=lifespan
)

# 🔹 Registrar middleware
app.add_middleware(TimerLoggingMiddleware)

# 🔹 Registrar routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(tags.router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente 🚀"}
