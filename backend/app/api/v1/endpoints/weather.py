

from fastapi import APIRouter, Depends, HTTPException

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from fastapi.security import OAuth2PasswordRequestForm

from backend.app.models.weather import WeatherResponse, WeatherPredictionResponse
from backend.app.db.repositories.weather import WeatherRepository
from backend.app.api.v1.dependencies.database import get_repository, get_api_key
from backend.app.utils.ai_model import predict_temperature_trend


router = APIRouter()


@router.get("/{city}/", response_model=WeatherResponse, name="users:get-weather-by-city")
async def get_weather_by_city(
        query: str,  # query parameter for the city
        city: str,  # Path parameter for the city
        weather_repo: WeatherRepository = Depends(get_repository(WeatherRepository))
) -> WeatherResponse:
    info = await weather_repo.get_weather_by_city(city=city, query=query)

    if not info:
        raise HTTPException(status_code=404, detail="City not found")

    return info


@router.get("/predict_temperature/{city}", response_model=WeatherPredictionResponse)
async def predict_temperature(query: str,
                              city: str,
                              api_key: str = Depends(get_api_key),
                              weather_repo: WeatherRepository = Depends(get_repository(WeatherRepository))):
    weather_data = await weather_repo.get_weather_by_city(city=city, query=query)
    current_temp = weather_data["main"]["temp"]
    predicted_temp = predict_temperature_trend(current_temp)
    return WeatherPredictionResponse(predicted_temperature=predicted_temp)

