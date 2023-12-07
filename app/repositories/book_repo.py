from uuid import UUID
from typing import List
from app.models.book import Book


class BookRepo:
    books = [
        Book(id=UUID('85db966c-67f1-411e-95c0-f02edfa5464a'),
             title='The Great Gatsby',
             author='F. Scott Fitzgerald',
             genre='Classic',
             publisher='Scribner',
             description='A novel depicting the luxurious lifestyle of the 1920s.',
             ),

        Book(id=UUID('31babbb3-5541-4a2a-8201-537cdff25fed'),
             title='To Kill a Mockingbird',
             author='Harper Lee',
             genre='Fiction',
             publisher='J.B. Lippincott & Co.',
             description='A classic novel set in the American South during the 1930s, dealing with racial injustice.'),

        Book(id=UUID('45309954-8e3c-4635-8066-b342f634252c'),
             title='1984',
             author='George Orwell',
             genre='Dystopian',
             publisher='Secker & Warburg',
             description='A dystopian novel depicting a totalitarian regime and its impact on society.')
    ]

    def get_books(self) -> List[Book]:
        return self.books

    def get_book_by_id(self, book_id: UUID) -> Book:
        return next((book for book in self.books if book.id == book_id), None)

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
