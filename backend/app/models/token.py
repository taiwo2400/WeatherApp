from datetime import datetime, timedelta
from pydantic import EmailStr

from backend.app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.models.core import CoreModel


class JWTMeta(CoreModel):
    iss: str = "weather_app.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


class EmailVerificationMeta(CoreModel):
    iss: str = "weather_app.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    token_type: str


class JWTCreds(CoreModel):
    """How we'll identify users"""
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCreds):
    """
    JWT Payload right before it's encoded - combine meta and username
    """
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str


class EmailVerificationCreds(CoreModel):
    sub: str


class JWTEmailVerificationPayload(EmailVerificationMeta, EmailVerificationCreds):
    pass
