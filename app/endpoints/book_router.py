import uuid
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.book_catalog_service import BookCatalogService
from app.models.book import Book, CreateBookRequest

book_catalog_router = APIRouter(prefix='/book-catalog', tags=['BookCatalog'])


@book_catalog_router.get('/')
def get_books(book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> list[Book]:
    return book_catalog_service.get_books()


@book_catalog_router.get('/{book_id}')
def get_book(book_id: UUID, book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    book = book_catalog_service.get_book_by_id(book_id)
    if book:
        return book.dict()
    else:
        raise HTTPException(404, f'Book with id={book_id} not found')


@book_catalog_router.post('/add')
def add_book(request: CreateBookRequest,
             book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    new_book = book_catalog_service.add_book(request.title, request.author, request.genre, request.publisher,
                                             request.description)
    return new_book.dict()


@book_catalog_router.put('/update/{book_id}')
def update_book(book_id: UUID, request: CreateBookRequest,
                book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> Book:
    updated_book = book_catalog_service.update_book(book_id, request.title, request.author, request.genre,
                                                    request.publisher, request.description)
    return updated_book.dict()


@book_catalog_router.delete('/delete/{book_id}')
def delete_book(book_id: UUID, book_catalog_service: BookCatalogService = Depends(BookCatalogService)) -> None:
    book_catalog_service.delete_book(book_id)
    return {'message': 'Book deleted successfully'}
