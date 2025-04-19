"""User Models that validate the data for User endpoints."""

import string
from typing import Optional
from enum import Enum

from pydantic import EmailStr, constr, field_validator

from backend.app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from backend.app.models.token import AccessToken


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username


class UserType(str, Enum):
    customer = "customer"
    staff = "staff"


class ContactType(str, Enum):
    phone = "phone"
    email = "email"
    other = "other"


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """
    email: Optional[EmailStr]
    username: Optional[str]

    @field_validator("username")
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserBase(CoreModel):
    """
    All common characteristics of our users
    """
    firstname: str
    middle_name: Optional[str]
    lastname: str
    username: str
    email: EmailStr
    email_verified: Optional[bool] = False
    password: str
    usertype: UserType = UserType.staff
    phone_number: str
    street: str
    city: str
    state: str


class UserCreate(UserBase):
    way_to_contact: Optional[ContactType]
    password: constr(min_length=7, max_length=100)
    username: str

    @field_validator("username")
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models like dicts


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    salt: Optional[str] = None


class UserPasswordUpdate(CoreModel):
    """
    Users can create or change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken] = None

