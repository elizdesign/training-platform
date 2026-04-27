import sys
from pathlib import Path
import bcrypt

# Добавляем корень проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

# Импортируем НАПРЯМУЮ (не через __init__.py)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

# Настройки БД
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fitness_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Определяем модели ПРЯМО ЗДЕСЬ (чтобы не было конфликтов импорта)
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class RoleModel(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def recreate_db():
    print("⚠️  Начинаем перезагрузку БД...")

    # Удаляем таблицы
    print("🗑️  Удаляем старые таблицы...")
    Base.metadata.drop_all(bind=engine)

    # Создаём заново
    print("🔨 Создаём новые таблицы...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы.")

    # Заполняем
    print("📝 Заполняем данными...")
    with engine.connect() as conn:
        # Роли
        conn.execute(text("INSERT INTO roles (id, name) VALUES (1, 'admin')"))
        conn.execute(text("INSERT INTO roles (id, name) VALUES (2, 'trainer')"))
        conn.commit()

        # Админ
        password = "admin123"
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_superuser, role_id)
            VALUES ('admin@fitness.com', :pwd, 'Admin User', TRUE, 1)
        """), {"pwd": hashed_pw})
        conn.commit()

    print("👤 Админ: admin@fitness.com / admin123")
    print("🎉 Готово!")


if __name__ == "__main__":
    recreate_db()