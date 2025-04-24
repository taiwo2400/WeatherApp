from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.status import HTTP_200_OK

from backend.app.models.version import VersionInfo
from backend.app.core import config
from backend.app.utils.logging_config import get_logger

log = get_logger()

router = APIRouter()


@router.get(
    "/",
    response_model=VersionInfo,
    name="version:get-current-version",
    status_code=HTTP_200_OK
)
async def get_current_version() -> VersionInfo:
    log.info("Weather App Version requested", service="get-current-version")
    return VersionInfo.parse_obj(
        {
            "version": config.version,
            "release_date": config.release_date,
            "status": config.status,
            "commit_hash": config.commit_hash,
            "server": config.server,
            "environment": config.environment,
            "uptime": config.uptime,
            "documentation_url": config.changelog_url,
            "changelog_url": config.changelog_url,
            "license": config.license,
            "contact": config.contact
        }
    )


@router.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    log.info("weather_app Version requested", service="get-current-version")
    return FileResponse("openapi.yaml", media_type="text/yaml")
