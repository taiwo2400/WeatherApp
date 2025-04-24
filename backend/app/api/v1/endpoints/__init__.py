from fastapi import APIRouter

from backend.app.api.v1.endpoints.app_info import router as version_router
from backend.app.api.v1.endpoints.weather import router as weather_router


router = APIRouter()

router.include_router(version_router, prefix="/version-info", tags=["version"])
router.include_router(weather_router, prefix="/weather", tags=["weather"])

