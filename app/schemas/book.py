from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    description = Column(String, nullable=False)
