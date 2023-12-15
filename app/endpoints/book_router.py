from uuid import UUID

import keycloak
from keycloak import KeycloakOpenID
from typing import Optional, Callable

from app.auth.keycloak_auth import KeycloakAuthenticator
from app.creds import *

from functools import wraps
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.models.book import Book, CreateBookRequest
from app.services.book_catalog_service import BookCatalogService

book_catalog_router = APIRouter(prefix='/book-catalog', tags=['BookCatalog'])

keycloak_authenticator = KeycloakAuthenticator()

access_tokens = {}

keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=keycloak_client_id,
    client_secret_key=keycloak_client_secret,
    realm_name="uzorov",
    verify=False
)


def get_current_user(token: str):
    try:
        user_info = keycloak_openid.userinfo(token=token)
    except keycloak.exceptions.KeycloakAuthenticationError:
        raise HTTPException(status_code=403, detail={"details:": "Your access token is not valid"})

    return user_info


@book_catalog_router.get("/login")
def login(request: Request):
    response_content = keycloak_authenticator.login()
    return response_content


@book_catalog_router.get("/callback")
async def callback(request: Request):
    access_token = await keycloak_authenticator.callback(request)
    user_info = get_current_user(access_token)
    access_tokens.update({access_token: user_info})

    user = get_current_user(access_token)

    realm_access = user.get("realm_access", [])
    roles = realm_access.get("roles", [])

    response_message = f"""
                                                                   <html>
                                                                       <head>
                                                                           <title>Your token</title>
                                                                           <style>
                                                                               body {{
                                                                                   font-size: 27px;
                                                                                   color: orange;
                                                                                   text-align: center;
                                                                                   
                                                                               }}
                                                                               p {{
    word-break: break-all;
    white-space: normal;
}}
                                                                           </style>
                                                                       </head>
                                                                       <body>
                                                                    
                                                                           <p style="color: black;" >You're authorized now. Please use your token to get access to the services:</p>
                                                                            <p style="font-weight: bold;">{access_token}</p>
                                                                            <p style="color: black;">You may use service with next roles: {roles}</p>
                                                                              <a href="http://localhost:8000/docs#">Go to DOCS</a>
                                                                       </body>
                                                                   </html>
                                                               """

    return HTMLResponse(response_message)


def keycloak_security(required_roles: Optional[list] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
                *args,
                **kwargs):

            token = kwargs.get("token")

            if token:
                user = get_current_user(token)

                realm_access = user.get("realm_access", [])
                roles = realm_access.get("roles", [])

                if not any(role in roles for role in required_roles):
                    error_message = f"""
                                                                                   <html>
                                                                                       <head>
                                                                                           <title>Insufficient permissions</title>
                                                                                           <style>
                                                                                               body {{
                                                                                                   font-size: 27px;
                                                                                                   color: black;
                                                                                                   text-align: center;
                                                                                               }}
                                                                                           </style>
                                                                                       </head>
                                                                                       <body>
                                                                                           <p>Permission for your role denied</p>
                                                                                           <p>You may use service only with next roles: {roles}</p>
                                                                                           <a href="http://localhost:8000/book-api/book-catalog/login">Login</a>
                                                                                       </body>
                                                                                   </html>
                                                                               """
                    return HTMLResponse(content=error_message, status_code=403)

            else:
                error_message = f"""
                                                               <html>
                                                                   <head>
                                                                       <title>Unauthorized Access</title>
                                                                       <style>
                                                                           body {{
                                                                               font-size: 33px;
                                                                               color: red;
                                                                               text-align: center;
                                                                           }}
                                                                       </style>
                                                                   </head>
                                                                   <body>
                                                                       <p>You're not authorized. Please login with this URL first:</p>
                                                                       <a href="http://localhost:8000/book-api/book-catalog/login">Login</a>
                                                                   </body>
                                                               </html>
                                                           """
                return HTMLResponse(content=error_message, status_code=403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


@book_catalog_router.get('/')
@keycloak_security(["admin", "user"])
def get_books(

        book_catalog_service: BookCatalogService = Depends(BookCatalogService),
        token: str = None,
):
    return book_catalog_service.get_books()


@book_catalog_router.get('/_test')
@keycloak_security(["admin"])
def get_user_info(token: str = None):
    return get_current_user(token)


@book_catalog_router.get('/{book_id}')
@keycloak_security(["admin", "user"])
def get_book(book_id: UUID,
             book_catalog_service: BookCatalogService = Depends(BookCatalogService), token: str = None) -> Book:
    book = book_catalog_service.get_book_by_id(book_id)
    if book:
        return book.model_dump()
    else:
        raise HTTPException(404, f'Book with id={book_id} not found')


@book_catalog_router.post('/add')
@keycloak_security(["admin"])
def add_book(request: CreateBookRequest,
             book_catalog_service: BookCatalogService = Depends(BookCatalogService),
             token: str = None, ) -> Book:
    new_book = book_catalog_service.add_book(request.title, request.author, request.genre, request.publisher,
                                             request.description)
    return new_book.dict()


@book_catalog_router.put('/update/{book_id}')
@keycloak_security(["admin"])
def update_book(book_id: UUID, request: CreateBookRequest,
                book_catalog_service: BookCatalogService = Depends(BookCatalogService), token: str = None) -> Book:
    updated_book = book_catalog_service.update_book(book_id, request.title, request.author, request.genre,
                                                    request.publisher, request.description)
    return updated_book.dict()


@book_catalog_router.delete('/delete/{book_id}')
@keycloak_security(["admin"])
def delete_book(book_id: UUID,
                book_catalog_service: BookCatalogService = Depends(BookCatalogService), token: str = None) -> None:
    book_catalog_service.delete_book(book_id)

    return {'message': 'Book deleted successfully'}
