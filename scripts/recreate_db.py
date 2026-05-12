import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text
from backend.db.base import Base
from backend.db.session import engine

# 🔴 ИМПОРТИРУЕМ ВСЕ МОДЕЛИ СЮДА (чтобы SQLAlchemy их увидел)
from backend.models.user import User, Role
from backend.models.client import Client
from backend.models.workout import Workout
from backend.models.exercise import Exercise
from backend.models.photo import ProgressPhoto
from backend.models.progress import Measurement

from backend.services.auth import get_password_hash
from sqlalchemy.orm import Session

def recreate_db():
    print("🗄️  Начинаем перезагрузку БД...")


def recreate_db():
    print("🔄 Начинаем перезагрузку БД...")

    # 1. Подключаемся и удаляем ВСЁ (с каскадом)
    print("🗑️ Удаляем старые таблицы...")
    with engine.connect() as conn:
        # Сначала удаляем зависимые таблицы
        conn.execute(text("DROP TABLE IF EXISTS clients CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS roles CASCADE"))
        conn.commit()
    print("✅ Таблицы удалены")

    # 2. Создаем новые таблицы через SQLAlchemy
    print("🏗️ Создаем новые таблицы...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")

    # 3. Заполняем данными
    print("📝 Заполняем данными...")
    with Session(engine) as session:
        # Создаем роли
        admin_role = Role(id=1, name="admin")
        trainer_role = Role(id=2, name="trainer")

        session.add(admin_role)
        session.add(trainer_role)
        session.commit()

        # Создаем админа
        admin_user = User(
            email="admin@fitness.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role_id=1,
            is_active=True  # Важно!
        )

        session.add(admin_user)
        session.commit()

        print("✅ Админ создан: admin@fitness.com / admin123")

    print("🎉 Готово!")


if __name__ == "__main__":
    recreate_db()