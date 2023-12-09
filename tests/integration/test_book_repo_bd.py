# /tests/integration/test_Book_repo_db.py

import pytest
from uuid import uuid4
from time import sleep
from datetime import datetime

from app.models.book import Book
from app.repositories.bd_books_repo import BookRepo

sleep(5)


@pytest.fixture()
def book_repo() -> BookRepo:
    repo = BookRepo()
    return repo


@pytest.fixture(scope='session')
def first_book() -> Book:
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    return Book(id=id, title=title, author=author, genre=genre,
                publisher=publisher, description=description)


@pytest.fixture(scope='session')
def second_book() -> Book:
    id = uuid4()
    title = 'Second Book Title'
    author = 'Second Author Name'
    genre = 'Comedy'
    publisher = 'Second Publisher Name'
    description = 'Second Book Description'

    return Book(id=id, title=title, author=author, genre=genre,
                publisher=publisher, description=description)


def test_empty_list(book_repo: BookRepo) -> None:
    assert book_repo.get_books() != []


def test_add_first_book(first_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.add_book(first_book) == first_book


def test_get_book_by_id(first_book: Book, book_repo: BookRepo) -> None:
    book = book_repo.get_books()[0]
    book_by_id = book_repo.get_book_by_id(book.id)
    assert book.id == book_by_id.id


def test_get_book_by_id_error(book_repo: BookRepo) -> None:
    with pytest.raises(KeyError):
        book_repo.get_book_by_id(uuid4())


def test_add_second_book(first_book: Book, second_book: Book, book_repo: BookRepo) -> None:
    assert book_repo.add_book(second_book) == second_book
    books = book_repo.get_books()
    assert books[len(books) - 1] == second_book


