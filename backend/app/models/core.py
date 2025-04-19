from typing import Optional

from datetime import datetime
from pydantic import BaseModel, field_validator


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here.
    """
    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @field_validator("created_at", "updated_at", mode="before")
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now()


class IDModelMixin(BaseModel):
    id: int
