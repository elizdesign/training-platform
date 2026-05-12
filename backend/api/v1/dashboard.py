## backend/api/v1/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.db.session import get_db
from backend.models.user import User
from backend.models.client import Client
from backend.models.workout import Workout
from backend.models.progress import Measurement
from backend.schemas.dashboard import DashboardResponse, ClientWithoutWorkout
from backend.services.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Количество активных клиентов
    total_active_clients = db.query(Client).filter(
        Client.trainer_id == current_user.id
    ).count()

    # 2. Количество тренировок за этот месяц
    first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total_workouts_this_month = db.query(Workout).filter(
        Workout.trainer_id == current_user.id,
        Workout.workout_date >= first_day_of_month.date()
    ).count()

    # 3. Количество измерений
    total_measurements = db.query(Measurement).join(Client).filter(
        Client.trainer_id == current_user.id
    ).count()

    # 4. Клиенты без тренировок больше 7 дней
    seven_days_ago = datetime.now() - timedelta(days=7)

    all_clients = db.query(Client).filter(Client.trainer_id == current_user.id).all()

    clients_without_workouts = []
    for client in all_clients:
        last_workout = db.query(Workout).filter(
            Workout.client_id == client.id
        ).order_by(Workout.workout_date.desc()).first()

        if not last_workout or last_workout.workout_date < seven_days_ago.date():
            days_since = 0
            if last_workout:
                days_since = (datetime.now().date() - last_workout.workout_date).days
            else:
                days_since = 999

            clients_without_workouts.append(
                ClientWithoutWorkout(
                    id=client.id,
                    first_name=client.first_name,
                    last_name=client.last_name,
                    phone=client.phone,
                    last_workout_date=last_workout.workout_date if last_workout else None,
                    days_since_last_workout=days_since
                )
            )

    # 5. Новых клиентов (просто возвращаем всех, т.к. нет created_at)
    # В будущем добавь поле created_at в модель Client
    recent_clients = []

    return DashboardResponse(
        total_active_clients=total_active_clients,
        total_workouts_this_month=total_workouts_this_month,
        total_measurements=total_measurements,
        clients_without_workouts=clients_without_workouts,
        recent_clients=recent_clients
    )