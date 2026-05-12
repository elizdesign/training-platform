# backend/api/v1/uploads.py
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.user import User
from backend.models.photo import ProgressPhoto
from backend.services.auth import get_current_user
from backend.schemas.photo import PhotoResponse

router = APIRouter(prefix="/uploads", tags=["Uploads"])

# Папка для хранения файлов (создай её в корне проекта!)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/progress", response_model=PhotoResponse)
async def upload_progress_photo(
    file: UploadFile = File(...),
    client_id: int = None,
    photo_type: str = "progress",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Валидация расширения
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    # 2. Генерация уникального имени
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # 3. Сохранение файла
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения: {str(e)}")

    # 4. Запись в БД
    # В реальном проекте тут стоит проверить, что client_id принадлежит текущему тренеру
    new_photo = ProgressPhoto(
        client_id=client_id,
        file_path=file_path, # В проде лучше хранить относительный путь или URL
        photo_type=photo_type
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)

    return new_photo