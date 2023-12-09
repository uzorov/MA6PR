# /tests/unit/test_delivery_service.py

import pytest
from uuid import uuid4, UUID
from datetime import datetime

from app.services.book_catalog_service import BookCatalogService
from app.repositories.book_repo import BookRepo


@pytest.fixture(scope='session')
def book_service() -> BookCatalogService:
    return BookCatalogService(BookRepo(clear=True))


@pytest.fixture()
def book_repo() -> BookRepo:
    return BookRepo()


@pytest.fixture(scope='session')
def first_book_data() -> tuple[UUID, str, str, str, str, str]:
    return uuid4(), 'title1', 'author1', 'genre1', 'publisher1', 'desc1'


@pytest.fixture(scope='session')
def second_book_data() -> tuple[UUID, str, str, str, str, str]:
    return uuid4(), 'title2', 'author2', 'genre2', 'publisher2', 'desc2'


def test_empty_books(book_service: BookCatalogService) -> None:
    assert book_service.get_books() == []


def test_add_book(
        first_book_data,
        book_service: BookCatalogService
) -> None:
    id, title, author, genre, publisher, desc = first_book_data
    book_service.add_book(title, author, genre, publisher, desc)
    book = book_service.get_books()[0]
    assert book.title == title
    assert book.author == author
    assert book.genre == genre
    assert book.publisher == publisher
    assert book.description == desc


def test_add_second_book(
        second_book_data,
        book_service: BookCatalogService
) -> None:
    id, title, author, genre, publisher, desc = second_book_data
    book_service.add_book(title, author, genre, publisher, desc)
    book = book_service.get_books()[1]
    assert book.title == title
    assert book.author == author
    assert book.genre == genre
    assert book.publisher == publisher
    assert book.description == desc


def test_get_books_full(
        first_book_data,
        second_book_data,
        book_service: BookCatalogService
) -> None:
    books = book_service.get_books()
    assert len(books) == 2
    assert books[0].title == first_book_data[1]
    assert books[1].title == second_book_data[1]


def test_get_books(book_service: BookCatalogService,
                   first_book_data: tuple[UUID, str, str, str, str, str],
                   second_book_data: tuple[UUID, str, str, str, str, str]) -> None:
    books = book_service.get_books()

    # Проверяем, что список книг не пустой и содержит ожидаемые книги
    assert books
    assert len(books) == 2
    # Добавим книги через book_service
    _, title1, author1, genre1, publisher1, desc1 = first_book_data
    _, title2, author2, genre2, publisher2, desc2 = second_book_data

    book_service.add_book(title1, author1, genre1, publisher1, desc1)
    book_service.add_book(title2, author2, genre2, publisher2, desc2)

    books_after_addition = book_service.get_books()
    assert len(books_after_addition) == 4

    # Проверяем, что данные книг соответствуют ожидаемым

    assert books_after_addition[2].title == first_book_data[1]
    assert books_after_addition[2].author == first_book_data[2]
    assert books_after_addition[2].genre == first_book_data[3]
    assert books_after_addition[2].publisher == first_book_data[4]
    assert books_after_addition[2].description == first_book_data[5]

    assert books_after_addition[3].title == second_book_data[1]
    assert books_after_addition[3].author == second_book_data[2]
    assert books_after_addition[3].genre == second_book_data[3]
    assert books_after_addition[3].publisher == second_book_data[4]
    assert books_after_addition[3].description == second_book_data[5]


def test_get_book_by_id(book_service: BookCatalogService,
                        first_book_data: tuple[UUID, str, str, str, str, str]) -> None:

    book = book_service.get_books()[0]
    first_book_id = book.id

    book = book_service.get_book_by_id(first_book_id)

    assert book.title == first_book_data[1]
    assert book.author == first_book_data[2]
    assert book.genre == first_book_data[3]
    assert book.publisher == first_book_data[4]
    assert book.description == first_book_data[5]
