# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import health, auth, clients, workouts
from backend.core.config import settings
from backend.db.base import Base
from backend.db.session import engine
from backend.api.v1 import health, auth, clients, workouts, imports
from backend.api.v1 import health, auth, clients, workouts, imports, uploads
from backend.api.v1 import health, auth, clients, workouts, imports, uploads, dashboard

# Настраиваем Swagger (OpenAPI)
app = FastAPI(
    title="Fitness Platform API",
    openapi_security_schemes={
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "api/v1/auth/login",  # <-- ВОТ ЭТО ИСПРАВЛЯЕТ ОШИБКУ
                    "scopes": {}
                }
            }
        }
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(workouts.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(uploads.router, prefix="/api/v1")

app.include_router(imports.router, prefix="/api/v1")