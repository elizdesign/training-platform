# backend/models/client.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.db.base import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    # Данные клиента
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    goal = Column(String(255), nullable=True)  # Например: "Похудеть", "Набрать массу"

    # Связь с тренером (User)
    # trainer_id — это внешний ключ на таблицу users
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связь "один ко многим": у одного тренера много клиентов
    trainer = relationship("User", back_populates="clients")

    workouts = relationship("Workout", back_populates="client")

    photos = relationship("ProgressPhoto", back_populates="client", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=datetime.utcnow)
    measurements = relationship("Measurement", back_populates="client", cascade="all, delete-orphan")