
from backend.app.core.config import CITY_BASE_URL, GEO_BASE_URL
from backend.app.models.weather import WeatherGetType


class BaseRepository:
    """
    simple class needed only to keep a reference to Weather API.
    In the future we can add functionality for common API actions

    """
    def __init__(self, request_type: str) -> None:
        if request_type == WeatherGetType.city:
            self.base_url = CITY_BASE_URL
        else:
            self.base_url = GEO_BASE_URL
