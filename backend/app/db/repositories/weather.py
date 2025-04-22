import requests
from typing import Optional

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from backend.app.db.repositories.base import BaseRepository
from backend.app.models.weather import WeatherInDB, WeatherRequestParams
from backend.app.models.user import UserInDB
from backend.app.core.config import config
from backend.app.services import auth_service
from backend.app.models.token import AccessToken

from backend.app.db.repositories.user_queries import (
    GET_USER_BY_USERNAME_QUERY,
    GET_USER_BY_EMAIL_QUERY,
    UPDATE_EMAIL_VERIFIED
)


class WeatherRepository(BaseRepository):
    """"
    All database actions associated with the Users resource
    """

    def __init__(self, request_type: str) -> None:
        super().__init__(request_type=request_type)
        self.auth_service = auth_service

    async def get_user_by_username(self, *, username: str, populate: bool = True) -> Optional[UserInDB]:
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_USERNAME_QUERY,
            values={"username": username},
        )

        if user_record:
            user = UserInDB(**user_record)

            return user

        return None

    async def get_weather_by_city(self, *, city: str, query: str) -> WeatherInDB:

        params = WeatherRequestParams.parse_obj(
            {
                "q": city,
                "appid": config.get("OPENWEATHER_API_KEY"),
                "units": query,
            })

        response = requests.get(self.base_url, params=params)

        try:
            response.raise_for_status()
            weather_data = response.json()

            return WeatherInDB.parse_obj(
                {
                    "city": weather_data["name"],
                    "country": weather_data.get("sys", {}).get("country"),
                    "temperature": weather_data["main"]["temp"],
                    "description": weather_data["weather"][0]["description"],
                    "humidity": weather_data["main"]["humidity"],
                    "pressure": weather_data["main"]["pressure"],
                    "wind_speed": weather_data["wind"]["speed"]
                }
            )

        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                raise HTTPException(status_code=404,
                                    detail="City not found")
            else:
                raise HTTPException(status_code=500,
                                    detail=f"Error fetching weather data: {e}")

        except (KeyError, IndexError) as e:
            raise HTTPException(status_code=500,
                                detail=f"Error parsing weather data: {e}. Check API response format.")

    async def verify_email(self, verification_token: AccessToken):
        decoded_token = self.auth_service.get_email_from_email_verification_token(token=verification_token.access_token)

        print(decoded_token)
        if decoded_token.token_type != "email_verification":
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_EMAIL_QUERY,
            values={"email": decoded_token.sub},
        )

        user_params = UserInDB(**user_record)

        if user_params.dict().get("email_verified"):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Email already verified. Click the link below to SignIn"
            )

        await self.db.fetch_one(
            query=UPDATE_EMAIL_VERIFIED,
            values={"email": decoded_token.sub},
        )
        return "Email verified successfully"
