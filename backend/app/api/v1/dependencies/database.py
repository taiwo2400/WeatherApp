"""I treat the Weather API as a database of weather records"""

from typing import Callable, Type

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKey, APIKeyHeader

from backend.app.db.repositories.base import BaseRepository
from backend.app.models.weather import WeatherAppURL
from backend.app.core.config import config


API_KEY_HEADER = APIKeyHeader(name="X-API-KEY")
API_KEY = config("OPENWEATHER_API_KEY")


def get_base_url(request_type: str, repo: BaseRepository = Depends(BaseRepository)) -> WeatherAppURL:
    """
    Get the base URL from the repository based on the request type.
    """
    return repo.base_url


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(request_url: str = Depends(get_base_url)) -> BaseRepository:
        repo_instance = repo_type(request_type=request_url)

        return repo_instance

    return get_repo


def get_api_key(api_key: APIKey = Depends(API_KEY_HEADER)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key
