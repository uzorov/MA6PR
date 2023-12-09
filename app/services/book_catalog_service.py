import uuid
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from app.models.book import Book
from app.repositories.bd_books_repo import BookRepo


class BookCatalogService:
    book_repo: BookRepo

    def __init__(self, book_repo: BookRepo = Depends(BookRepo)) -> None:
        self.book_repo = book_repo

    def get_books(self) -> List[Book]:
        return self.book_repo.get_books()

    def get_book_by_id(self, book_id: UUID) -> Book:
        return self.book_repo.get_book_by_id(book_id)

    def add_book(self, title: str, author: str, genre: str, publisher: str, description: str) -> Book:
        new_book = Book(id=uuid.uuid4(), title=title, author=author, genre=genre, publisher=publisher, description=description)
        return self.book_repo.add_book(new_book)

    def update_book(self, book_id: UUID, title: str, author: str, genre: str, publisher: str, description: str) -> Book:
        book = self.book_repo.get_book_by_id(book_id)
        book.title = title
        book.author = author
        book.genre = genre
        book.publisher = publisher
        book.description = description
        return self.book_repo.update_book(book)

    def delete_book(self, book_id: UUID) -> None:
        self.book_repo.delete_book(book_id)
