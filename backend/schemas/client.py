# backend/schemas/client.py
from pydantic import BaseModel
from typing import Optional

# Схема для создания клиента (входные данные)
class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    age: Optional[int] = None
    goal: Optional[str] = None

# Схема ответа (что возвращаем в JSON)
class ClientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    age: Optional[int] = None
    goal: Optional[str] = None
    trainer_id: int

    class Config:
        from_attributes = True # Нужно для SQLAlchemy 2.0+

