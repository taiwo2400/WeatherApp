import jwt
import bcrypt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from typing import Optional, Type

from fastapi import HTTPException, status
from pydantic import ValidationError

from backend.app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.models.token import (JWTMeta, JWTCreds, JWTPayload, JWTEmailVerificationPayload,
                              EmailVerificationCreds, EmailVerificationMeta)
from backend.app.models.user import UserPasswordUpdate, UserBase


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception that can be modified later on.
    """
    pass


class AuthService:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    def create_access_token_for_user(
            self,
            *,
            user: Type[UserBase],
            secret_key: str = str(SECRET_KEY),
            audience: str = JWT_AUDIENCE,
            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> Optional[str]:
        if not user or not isinstance(user, UserBase):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
        )
        access_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)

        return access_token

    def get_username_from_token(self, *, token: str, secret_key: str) -> Optional[str]:

        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload.username

    def get_email_from_token(self, *, token: str) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE)
            payload = JWTPayload(**decoded_token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid token")
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload.sub

    def get_email_from_email_verification_token(self, *, token: str) -> Optional[JWTEmailVerificationPayload]:
        try:
            decoded_token = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE)
            payload = JWTEmailVerificationPayload(**decoded_token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=400, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid token")
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    def create_email_verification_token(self, email: str,
            secret_key: str = str(SECRET_KEY),
            audience: str = JWT_AUDIENCE,
            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,) -> str:
        # Get current time in UTC and add 1 hour for expiration
        current_time = datetime.utcnow()
        expiration_time = current_time + timedelta(hours=1)

        jwt_meta = EmailVerificationMeta(
            aud=audience,
            iat=int((current_time - timedelta(hours=6)).timestamp()),
            exp=int(expiration_time.timestamp()),
            token_type=str("email_verification")
        )

        email_verification_creds = EmailVerificationCreds(sub=email)

        token_payload = JWTEmailVerificationPayload(
            **jwt_meta.dict(),
            **email_verification_creds.dict(),
        )
        verification_token = jwt.encode(token_payload.dict(), secret_key, algorithm=JWT_ALGORITHM)

        return verification_token

    def decode_email_verification_token(self, token: str):
        return jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE)
