from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ExerciseCreate(BaseModel):
    name: str
    sets: int = 3
    reps: int = 10
    weight: Optional[float] = None

class WorkoutCreate(BaseModel):
    title: str
    workout_date: date
    client_id: int
    exercises: List[ExerciseCreate] = []

class ExerciseResponse(BaseModel):
    id: int
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None
    workout_id: int

    class Config:
        from_attributes = True

class WorkoutResponse(BaseModel):
    id: int
    title: str
    workout_date: date
    client_id: int
    trainer_id: int
    exercises: List[ExerciseResponse] = []

    class Config:
        from_attributes = True