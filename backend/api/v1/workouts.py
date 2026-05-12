
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.user import User
from backend.models.client import Client
from backend.models.workout import Workout
from backend.models.exercise import Exercise
from backend.schemas.workout import WorkoutCreate, WorkoutResponse
from backend.services.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
def create_workout(
        workout_data: WorkoutCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 1. Проверяем, что клиент существует и принадлежит текущему тренеру
    client = db.query(Client).filter(
        Client.id == workout_data.client_id,
        Client.trainer_id == current_user.id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Client not found or you don't have permission"
        )

    # 2. Создаем тренировку
    new_workout = Workout(
        title=workout_data.title,
        workout_date=workout_data.workout_date,
        client_id=client.id,
        trainer_id=current_user.id
    )

    db.add(new_workout)
    db.flush()  # Получаем ID тренировки без полного коммита, чтобы привязать упражнения

    # 3. Добавляем упражнения к тренировке
    for ex_data in workout_data.exercises:
        new_exercise = Exercise(
            workout_id=new_workout.id,
            **ex_data.model_dump()  # Pydantic v2 метод для преобразования в dict
        )
        db.add(new_exercise)

    # 4. Фиксируем всё в БД
    db.commit()
    db.refresh(new_workout)
    return new_workout


@router.get("/", response_model=list[WorkoutResponse])
def get_workouts(
        client_id: int | None = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Возвращаем только тренировки текущего тренера
    query = db.query(Workout).filter(Workout.trainer_id == current_user.id)

    # Опциональный фильтр по клиенту
    if client_id:
        query = query.filter(Workout.client_id == client_id)

    return query.all()