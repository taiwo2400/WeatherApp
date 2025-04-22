from datetime import date

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

CITY_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
GEO_BASE_URL = "http://api.openweathermap.org/data/2.5"
PROJECT_NAME = "Weather-App"
VERSION = "1.0.0"
API_PREFIX = "/api"
GIT_AUTH = "Adaramola Omolewa"
GIT_MESSAGE = "You are doing great"
DEPLOY_DATE = date.today()

version = "1.0.0"
release_date = "2025-03-18"
status = "API Status"
commit_hash = "abc123def456gh789"
changelog_url ="https://omolewa.com/changelog" # to keep track of the changes in the API/bug fixes
server ="FastAPI"
environment ="production"
uptime = "72 hours"
documentation_url ="https://omolewa.com/docs"
license ="OMOLEWA Licence"
contact = {"name": "Omolewa Adaramola", "email": "omolewa.davids@gmail.com"}


SECRET_KEY = config("SECRET_KEY", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast=int,
    default=7 * 24 * 60  # one week
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="weather_app:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")
