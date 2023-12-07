from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Review(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    book_id: UUID
    rating: int
    comment: str
    created_at: datetime
