from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.db.base import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    workout_date = Column(Date, nullable=False)

    # Связи
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    client = relationship("Client", back_populates="workouts")
    trainer = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")