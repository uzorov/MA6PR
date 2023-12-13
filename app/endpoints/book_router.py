import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.book_catalog_service import BookCatalogService
from app.models.book import Book, CreateBookRequest
from fastapi import Response

import prometheus_client

book_catalog_router = APIRouter(prefix='/book-catalog', tags=['BookCatalog'])
metrics_router = APIRouter(tags=['Metrics'])

get_books_count = prometheus_client.Counter(
    "get_books_count",
    "Number of get requests for books"
)

get_book_count = prometheus_client.Counter(
    "get_book_count",
    "Number of get requests for book by id"
)

add_book_count = prometheus_client.Counter(
    "add_book_count",
    "Number of created books"
)
update_book_count = prometheus_client.Counter(
    "update_book_count",
    "Number of updated books"
)

delete_book_count = prometheus_client.Counter(
    "delete_book_count",
    "Number of deleted books"
)

failed_get_book_count = prometheus_client.Counter(
    "failed_get_book_count",
    "Number of failed attempts to get book by id"
)


@book_catalog_router.get('/')
def get_books(book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> list[Book]:
    get_books_count.inc(1)
    return book_catalog_service.get_books()


@book_catalog_router.get('/{book_id}')
def get_book(book_id: UUID, book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    book = book_catalog_service.get_book_by_id(book_id)
    get_book_count.inc(1)
    if book:
        return book.dict()
    else:
        failed_get_book_count.inc(1)
        raise HTTPException(404, f'Book with id={book_id} not found')


@book_catalog_router.post('/add')
def add_book(request: CreateBookRequest,
             book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    add_book_count.inc(1)
    new_book = book_catalog_service.add_book(request.title, request.author, request.genre, request.publisher,
                                             request.description)
    return new_book.dict()


@book_catalog_router.put('/update/{book_id}')
def update_book(book_id: UUID, request: CreateBookRequest,
                book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    updated_book = book_catalog_service.update_book(book_id, request.title, request.author, request.genre,
                                                    request.publisher, request.description)
    update_book_count.inc(1)
    return updated_book.dict()


@book_catalog_router.delete('/delete/{book_id}')
def delete_book(book_id: UUID, book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> None:
    book_catalog_service.delete_book(book_id)
    delete_book_count.inc(1)
    return {'message': 'Book deleted successfully'}


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
