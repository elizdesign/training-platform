# backend/schemas/dashboard.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ClientWithoutWorkout(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    last_workout_date: Optional[datetime] = None
    days_since_last_workout: int

class DashboardResponse(BaseModel):
    total_active_clients: int
    total_workouts_this_month: int
    total_measurements: int
    clients_without_workouts: List[ClientWithoutWorkout]
    recent_clients: List[dict]  # Новых клиентов за последнюю неделю

    class Config:
        from_attributes = True