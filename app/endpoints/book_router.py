from uuid import UUID
from typing import Optional
from uuid import UUID

import httpx
import requests
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse

from app.models.book import Book, CreateBookRequest
from app.services.book_catalog_service import BookCatalogService

keycloak_authorization_url = "http://localhost:8080/realms/uzorov/protocol/openid-connect/auth"
keycloak_token_url = "http://localhost:8080/realms/uzorov/protocol/openid-connect/token"
keycloak_user_info_url = "http://localhost:8080/realms/uzorov/protocol/openid-connect/userinfo"
keycloak_client_id = "uzorov-client"
keycloak_client_secret = "oVS88q2j5FMjUOuIwLGRuYN0NVUxaXk8"
keycloak_redirect_uri = "http://localhost:8000/book-api/book-catalog/callback"
keycloak_state = "uzorov123"

book_catalog_router = APIRouter(prefix='/book-catalog', tags=['BookCatalog'])


@book_catalog_router.get("/login")
async def login(request: Request):
    # Manually specify redirect_uri and state

    # Construct the authorization URL with the specified parameters
    authorization_url = (f"{keycloak_authorization_url}?response_type=code&client_id={keycloak_client_id}&redirect_uri="
                         f"{keycloak_redirect_uri}&state={keycloak_state}&client_secret={keycloak_client_secret}&"
                         f"scope=openid profile")

    # Redirect the user to the authorization URL
    return RedirectResponse(url=authorization_url)


@book_catalog_router.get("/callback")
async def callback(request: Request):
    # Получили код для получения токена
    code = request.query_params.get("code")

    if code:
        # Now you have the authorization code, and you can use it to obtain the access token

        data = {
            "grant_type": "authorization_code",
            "client_id": keycloak_client_id,
            "client_secret": keycloak_client_secret,
            "code": code,
            "redirect_uri": keycloak_redirect_uri,
            "scope": "openid profile",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(keycloak_token_url, data=data)

        # Handle the response from the token endpoint
        if response.status_code == 200:
            token_data = response.json()
            # Extract and return only the access token
            access_token = token_data.get("access_token")
            if access_token:

                # Получаем пользователя
                headers = {"Authorization": f"Bearer {access_token}"}

                async with httpx.AsyncClient() as client:
                    response = await client.get(keycloak_user_info_url, headers=headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    # Handle the error response, raise an exception, or return an appropriate result
                    return access_token

            else:
                raise HTTPException(status_code=500, detail="Access token not found in the response")
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to obtain access token {response.status_code} {response.json()}")
    else:
        raise HTTPException(status_code=400, detail="Authorization code not found in the query parameters")


def get_current_user(authorization: str = Depends(login)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(authorization,
                             "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJydkNZRlFtaVpBSFA1cUk4LUNnSjJuWmRVU0c1TGRuYm5VMkFjS0l6M0h3In0.eyJleHAiOjE3MDI0ODQ4NjAsImlhdCI6MTcwMjQ4NDU2MCwianRpIjoiMDk5ZWY4MDgtOTY3Ni00MTk5LTljZGEtNWQzYmJjMWNjMTc4IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy91em9yb3YiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYjI1NWM0MzgtMGQwMC00NWEwLTgzZTUtYzVkYmFmYTJhNzIxIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoidXpvcm92LWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI4MTY4ZTlmMi0zMjAyLTQ4MzItYjM4Yi1hNzFiYTFjYTM2NzAiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJlZGl0b3IiLCJvZmZsaW5lX2FjY2VzcyIsImFkbWluIiwiZGVmYXVsdC1yb2xlcy11em9yb3YiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGFkZHJlc3MgcGhvbmUgcm9sZXMgbWljcm9wcm9maWxlLWp3dCBvZmZsaW5lX2FjY2VzcyBwcm9maWxlIGVtYWlsIiwic2lkIjoiODE2OGU5ZjItMzIwMi00ODMyLWIzOGItYTcxYmExY2EzNjcwIiwidXBuIjoidXpvcm92LXVzZXIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYWRkcmVzcyI6e30sIm5hbWUiOiLQmtC40YDQuNC70Lsg0KPQt9C-0YDQvtCyIiwiZ3JvdXBzIjpbImVkaXRvciIsIm9mZmxpbmVfYWNjZXNzIiwiYWRtaW4iLCJkZWZhdWx0LXJvbGVzLXV6b3JvdiIsInVtYV9hdXRob3JpemF0aW9uIl0sInByZWZlcnJlZF91c2VybmFtZSI6InV6b3Jvdi11c2VyIiwiZ2l2ZW5fbmFtZSI6ItCa0LjRgNC40LvQuyIsImZhbWlseV9uYW1lIjoi0KPQt9C-0YDQvtCyIiwiZW1haWwiOiJ1em9yb3ZfMDJAbWFpbC5ydSJ9.nKYA_BOWD4bmENDtiaWNC4acSntVRnCJ3MDxPYbacicvTkgQhfbxp49QxHyD__K2cENUMEMP1Yg4Hb1l_w4OnSXR8v5TDUruE1SmlhJfwpJI64wGJsse24M5FOw5zmagHdkgPCO4F-zkmOQMU6OlfcvZNL2XR13oHgz0HdENEuLo8LHkgtD9KxaR6T9dx7zqb8KCiye3eM9P5MBgY24jF12c_MXVqG3R-JQy7U57torX790tF0avElwvFEh7pz2BRbtFeIdC6UeAaYzl_tj3hlD2p-USMpUnkAl030p4A_vZJv2lt0luTAGybBqO140696fH_WGvvoaFeHEMsTG_dw",
                             algorithms=["RS256"])
        token_data = payload.get("sub")
        if token_data is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_info_by_access_token(access_token=authorization)
    if user is None:
        raise credentials_exception

    return user


def keycloak_security(required_roles: Optional[list] = None):
    def decorator(func):
        def wrapper(*args, current_user: dict = Depends(get_current_user), **kwargs):
            if required_roles:
                user_roles = current_user.get("roles", [])
                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(status_code=403, detail="Insufficient permissions")

            return func(*args, current_user=current_user, **kwargs)

        return wrapper

    return decorator


# Example usage of the decorator:
@book_catalog_router.get('/gpt-test')
@keycloak_security(required_roles=["admin"])
def get_user_info(current_user: dict = Depends(get_current_user)):
    return current_user


def get_user_info_by_access_token(access_token: str):
    url = "http://localhost:8080/realms/uzorov/protocol/openid-connect/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@book_catalog_router.get('/test')
def get_user_info(user: dict = Depends(get_user_info_by_access_token)) -> dict:
    return user


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
