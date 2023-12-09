from uuid import uuid4

import pytest

from app.models.book import Book
from app.repositories.book_repo import BookRepo


@pytest.fixture(scope='session')
def book_repo() -> BookRepo:
    return BookRepo(clear=True)


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


book_test_repo = BookRepo()


def test_empty_list() -> None:
    assert book_test_repo.get_books() == []


def test_add_first_book(first_book: Book) -> None:
    book_test_repo.add_book(first_book)
    assert book_test_repo.get_books()[0] == first_book


def test_get_book_by_id(first_book: Book) -> None:
    assert book_test_repo.get_book_by_id(first_book.id) == first_book


def test_get_book_by_id_error() -> None:
    with pytest.raises(KeyError):
        book_test_repo.get_book_by_id(uuid4())


def test_add_second_book(first_book: Book, second_book: Book) -> None:
    assert book_test_repo.add_book(second_book) == second_book
    books = book_test_repo.get_books()
    assert len(books) == 2
    assert books[0] == first_book
    assert books[1] == second_book



