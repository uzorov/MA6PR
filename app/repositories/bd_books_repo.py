import traceback
import uuid
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas.book import Book as DBook


class BookRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, book: DBook) -> Book:
        result = Book.from_orm(book)
        # if task.book is not 0:
        #     result.book = self.book_repo.get_book_by_id(
        #         task.book)

        return result

    def _map_to_schema(self, book: Book) -> Book:
        data = dict(book)
        del data['id']
        data['id'] = book.id if book.id is not 0 else 0
        result = DBook(**data)
        return result

    def get_books(self) -> list[Book]:
        books = []
        # Book(id=uuid.uuid4(), title="Help me", author="fdafsf", genre="dfsdf", publisher="fdfs", description="dfsd")]

        for b in self.db.query(DBook).all():
            books.append(self._map_to_model(b))
        return books

    def get_book_by_id(self, id: UUID) -> Book:
        book = self.db \
            .query(DBook) \
            .filter(DBook.id == id) \
            .first()

        if book is None:
            raise KeyError

        return Book.from_orm(book)

    def add_book(self, book: Book) -> Book:
        try:
            db_book = self._map_to_schema(book)
            self.db.add(db_book)
            self.db.commit()
            return self._map_to_model(db_book)
        except:
            traceback.print_exc()
            raise KeyError
