from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.base import Base

class ProgressPhoto(Base):
    __tablename__ = "progress_photos"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    file_path = Column(String(255), nullable=False) # Путь к файлу на сервере
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    photo_type = Column(String(50), default="progress") # e.g., 'before', 'after'

    client = relationship("Client", back_populates="photos")