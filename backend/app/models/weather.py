"""Author: Adaramola, Bukola Omolewa"""

from backend.app.models.core import CoreModel

from enum import Enum


class WeatherResponse(CoreModel):
    temperature: float
    description: str
    humidity: float
    pressure: float
    country: str
    wind_speed: float


class WeatherPredictionResponse(CoreModel):
    will_temperature_rise: bool


class WeatherGetType(str, Enum):
    geo_loc = "geolocation"
    city = "city"


class WeatherAppURL(CoreModel):
    app_url: str
    request_type: WeatherGetType


class WeatherInDB(WeatherResponse):
    pass


class WeatherRequestParams(CoreModel):
    query: str
    appid: str
    units: str


class WeatherUnits(str, Enum):
    metric = "metric"
    imperial = "imperial"
