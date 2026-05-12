# backend/api/v1/clients.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.user import User
from backend.models.client import Client
from backend.schemas.client import ClientCreate, ClientResponse
from backend.services.auth import get_current_user

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
        client_data: ClientCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Проверяем, нет ли уже такого номера
    existing = db.query(Client).filter(Client.phone == client_data.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    # Создаем нового клиента и привязываем к текущему юзеру (тренеру)
    new_client = Client(
        **client_data.dict(),
        trainer_id=current_user.id
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/", response_model=list[ClientResponse])
def get_my_clients(
        skip: int = Query(0, ge=0, description="Сколько пропустить (для пагинации)"),
        limit: int = Query(20, ge=1, le=100, description="Сколько вернуть (макс. 100)"),
        search: str | None = Query(None, description="Поиск по имени, фамилии или телефону"),
        goal: str | None = Query(None, description="Фильтр по цели (например: 'похудеть')"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Базовый запрос: только клиенты текущего тренера
    query = db.query(Client).filter(Client.trainer_id == current_user.id)

    # 🔍 Поиск (case-insensitive)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Client.first_name.ilike(search_pattern)) |
            (Client.last_name.ilike(search_pattern)) |
            (Client.phone.ilike(search_pattern))
        )

    # 🎯 Фильтр по цели
    if goal:
        query = query.filter(Client.goal.ilike(f"%{goal}%"))

    # 📄 Пагинация + выполнение
    clients = query.offset(skip).limit(limit).all()
    return clients


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
        client_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Проверка безопасности: тренер может удалить только своего клиента
    if client.trainer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(client)
    db.commit()
    return None