from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import text

from alembic import context

from backend.db.base import Base
from backend.models.user import User, Role
from backend.models.client import Client
from backend.models.workout import Workout
from backend.models.exercise import Exercise
from backend.models.photo import ProgressPhoto
from backend.models.progress import Measurement


# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем metadata из твоих моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            "sqlalchemy.url": "postgresql+psycopg2://postgres:postgres@localhost:5432/fitness_db"
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Отладка
        result = connection.execute(text("SELECT current_database()"))
        db_name = result.scalar()
        print(f"\n🔍 ПОДКЛЮЧЕНИЕ К БАЗЕ: {db_name}")

        try:
            result2 = connection.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
            row = result2.fetchone()
            print(f"📦 ТЕКУЩАЯ РЕВИЗИЯ: {row[0] if row else 'НЕТ РЕВИЗИИ'}\n")
        except Exception:
            print("⚠️ Таблица alembic_version не найдена\n")

        # ==========================================
        # ГЛАВНОЕ: настраиваем контекст миграций
        # ==========================================
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()