from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.db.base import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    weight = Column(Float, nullable=True)

    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    workout = relationship("Workout", back_populates="exercises")