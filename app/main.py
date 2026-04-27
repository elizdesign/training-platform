from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import health, auth

app = FastAPI(title="Fitness Platform API", version="0.1.0")

app.include_router(health.router, prefix="/api/v1", tags=["Health Check"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

# ✅ РАСКОММЕНТИРУЙ ЭТУ СТРОКУ:
Base.metadata.create_all(bind=engine)