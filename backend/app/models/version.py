
from pydantic import Field

from backend.app.models.core import CoreModel


class Contact(CoreModel):
    name: str = Field(..., title="Support Contact Name")
    email: str = Field(..., title="Support Contact Email")


class VersionInfo(CoreModel):
    version: str = Field(..., title="API Version")
    release_date: str = Field(..., title="Release Date", example="2025-03-18")
    status: str = Field(..., title="API Status", example="production")
    commit_hash: str = Field(..., title="Current Commit Hash", example="abc123def456gh789")
    changelog_url: str = Field(..., title="Changelog URL", example="https://omolewa.com/changelog") # to keep track of the changes in the API/bug fixes
    server: str = Field(..., title="Server Technology", example="FastAPI")
    environment: str = Field(..., title="Environment", example="production")
    uptime: str = Field(..., title="API Uptime", example="72 hours")
    documentation_url: str = Field(..., title="Documentation URL", example="https://omolewa.com/docs")
    license: str = Field(..., title="API License", example="MIT")
    contact: Contact

    class Config:
        orm_mode = True  # Enables data parsing from ORMs if needed
