from sqlalchemy import create_engine, text
import hashlib

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fitness_db"

engine = create_engine(DATABASE_URL)


def simple_hash(password: str) -> str:
    """Простой хеш для теста (в продакшене используй bcrypt!)"""
    return f"hashed_{hashlib.sha256(password.encode()).hexdigest()}"


def main():
    print("🔧 Connecting...")

    with engine.connect() as conn:
        # Roles
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS roles (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
        """))

        conn.execute(text("INSERT INTO roles (id, name) VALUES (1, 'admin') ON CONFLICT (id) DO NOTHING"))
        conn.execute(text("INSERT INTO roles (id, name) VALUES (2, 'trainer') ON CONFLICT (id) DO NOTHING"))
        conn.commit()
        print("✅ Roles created")

        # Users
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                full_name VARCHAR(255),
                is_active BOOLEAN DEFAULT TRUE,
                is_superuser BOOLEAN DEFAULT FALSE,
                role_id INTEGER REFERENCES roles(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()

        # Admin
        result = conn.execute(text("SELECT id FROM users WHERE email = 'admin@fitness.com'"))
        if not result.fetchone():
            hashed = simple_hash("admin123")
            conn.execute(text("""
                INSERT INTO users (email, hashed_password, full_name, is_superuser, role_id)
                VALUES ('admin@fitness.com', :pwd, 'Admin', TRUE, 1)
            """), {"pwd": hashed})
            conn.commit()
            print("✅ Admin: admin@fitness.com / admin123")

        print("🎉 Done!")


if __name__ == "__main__":
    main()