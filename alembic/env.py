import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Importa tu Base con todos los modelos
from app.models.base import Base
from app.core.config import settings

# Configuración de logging de Alembic
config = context.config
fileConfig(config.config_file_name)

# Metadata de tus modelos
target_metadata = Base.metadata

# --- Funciones offline y online ---
def run_migrations_offline():
    """Ejecuta migraciones en modo offline (sin conexión a DB)"""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Ejecuta migraciones en modo online usando la conexión"""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Ejecuta migraciones en modo online (con AsyncEngine)"""
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
        echo=True,  # True para ver queries en consola
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# --- Ejecutar según el modo ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
