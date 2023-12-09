from uuid import UUID
from typing import List
from app.models.book import Book


class BookRepo:
    books = []

    def __init__(self, clear: bool = False) -> None:

        if clear:
            self.books = []

    def get_books(self) -> List[Book]:
        return self.books

    def get_book_by_id(self, book_id: UUID) -> Book:
        book = next((book for book in self.books if book.id == book_id), None)

        if book is not None:
            return book
        else:
            raise KeyError

    def add_book(self, book: Book) -> Book:
        self.books.append(book)
        return book

    def update_book(self, book: Book) -> Book:
        existing_book = next((b for b in self.books if b.id == book.id), None)
        if existing_book:
            existing_book.title = book.title
            existing_book.author = book.author
            existing_book.genre = book.genre
            existing_book.publisher = book.publisher
            existing_book.description = book.description
            existing_book.average_rating = book.average_rating
        return existing_book

    def delete_book(self, book_id: UUID) -> None:
        self.books = [book for book in self.books if book.id != book_id]
