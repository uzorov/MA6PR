# /tests/unit/test_book_model.py

import pytest
from uuid import uuid4
from pydantic import ValidationError

from app.models.book import Book, CreateBookRequest


def test_book_creation():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    book = Book(id=id, title=title, author=author, genre=genre,
                publisher=publisher, description=description)

    assert dict(book) == {'id': id, 'title': title, 'author': author,
                          'genre': genre, 'publisher': publisher, 'description': description}


def test_book_title_required():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    with pytest.raises(ValidationError):
        Book(id=id, author=author, genre=genre,
             publisher=publisher, description=description)


def test_book_author_required():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    with pytest.raises(ValidationError):
        Book(id=id, title=title, genre=genre,
             publisher=publisher, description=description)


def test_book_genre_required():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    with pytest.raises(ValidationError):
        Book(id=id, author=author, title=title,
             publisher=publisher, description=description)


def test_book_publisher_required():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    with pytest.raises(ValidationError):
        Book(id=id, author=author, genre=genre,
             title=title, description=description)


def test_book_desc_required():
    id = uuid4()
    title = 'Book Title'
    author = 'Author Name'
    genre = 'Fiction'
    publisher = 'Publisher Name'
    description = 'Book Description'

    with pytest.raises(ValidationError):
        Book(id=id, author=author, genre=genre,
             publisher=publisher, title=title)
