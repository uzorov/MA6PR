from fastapi import HTTPException

import httpx
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.creds import *


class KeycloakAuthenticator:

    def __init__(self):
        self._current_user = {}

    @property
    def current_user(self):
        return self._current_user

    def login(self):
        authorization_url = (
            f"{keycloak_authorization_url}?response_type=code&client_id={keycloak_client_id}&redirect_uri="
            f"{keycloak_redirect_uri}&state={keycloak_state}&client_secret={keycloak_client_secret}&"
            f"scope=openid profile")

        # Redirect the user to the authorization URL
        return RedirectResponse(url=authorization_url)

    async def callback(self, request: Request):
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

            if response.status_code == 200:
                token_data = response.json()

                access_token = token_data.get("access_token")
                if access_token:
                    return access_token

                    # Получаем пользователя
                    headers = {"Authorization": f"Bearer {access_token}"}

                    async with httpx.AsyncClient() as client:
                        response = await client.get(keycloak_user_info_url, headers=headers)

                    if response.status_code == 200:
                        self._current_user = response.json()
                        return response.json()
                    else:
                        return HTTPException(status_code=response.status_code,
                                             detail=f"Failed to obtain user info {response.status_code} {response.json()}")

                else:
                    raise HTTPException(status_code=500, detail="Access token not found in the response")
            else:
                raise HTTPException(status_code=response.status_code,
                                    detail=f"Failed to obtain access token {response.status_code} {response.json()}")
        else:
            raise HTTPException(status_code=400, detail="Authorization code not found in the query parameters")
