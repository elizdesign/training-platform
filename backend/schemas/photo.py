from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PhotoResponse(BaseModel):
    id: int
    client_id: int
    file_path: str
    uploaded_at: datetime
    photo_type: Optional[str] = None

    class Config:
        from_attributes = True