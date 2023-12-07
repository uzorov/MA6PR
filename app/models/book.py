from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    author: str
    genre: str
    publisher: str
    description: str


class CreateBookRequest(BaseModel):
    title: str
    author: str
    genre: str
    publisher: str
    description: str
