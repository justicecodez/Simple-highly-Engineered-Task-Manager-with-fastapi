from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from uuid import uuid4

from jose import JWTError, ExpiredSignatureError, jwt

from app.settings.jwt import jwt_settings 
from app.schema.user_schema import UserSchema

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a short-lived access token.
    Used for API authentication.
    """

    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(
            minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "iat": now,
        "exp": expire,
        "type": "access",
        "jti": str(uuid4()),
    })

    encoded_jwt = jwt.encode(
        to_encode,
        jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    data: dict
) -> Tuple[str, str]:
    """
    Creates a long-lived refresh token.

    Returns:
        token: JWT refresh token
        jti: unique token identifier for revocation tracking
    """

    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    jti = str(uuid4())

    to_encode.update({
        "iat": now,
        "exp": expire,
        "type": "refresh",
        "jti": jti,
    })

    encoded_jwt = jwt.encode(
        to_encode,
        jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )

    return encoded_jwt, expire


def decode_token(
    token: str
) -> Optional[dict]:
    """
    Decodes and verifies JWT signature.

    Returns:
        Payload dictionary if valid.
        None if invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            algorithms=[
                jwt_settings.ALGORITHM
            ]
        )

        # Required claims validation
        required_claims = [
            "user_id",
            "type",
            "jti",
            "iat",
            "exp",
        ]

        for claim in required_claims:
            if claim not in payload:
                return None

        return payload


    except ExpiredSignatureError:
        return None

    except JWTError:
        return None


def verify_token_type(
    payload: dict,
    expected_type: str
) -> bool:
    """
    Ensures token is the expected type.
    Prevents using refresh tokens as access tokens.
    """

    return payload.get("type") == expected_type


def verify_access_token(
    token: str
) -> Optional[dict]:
    """
    Validates an access token.
    """

    payload = decode_token(token)

    if not payload:
        return None

    if not verify_token_type(
        payload,
        "access"
    ):
        return None

    return payload


def verify_refresh_token(
    token: str
) -> Optional[dict]:
    """
    Validates a refresh token.
    """

    payload = decode_token(token)

    if not payload:
        return None

    if not verify_token_type(
        payload,
        "refresh"
    ):
        return None

    return payload
    """Verify that a token is of the expected type (access/refresh)."""
         
def get_current_user_from_token(token:str=Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")))->str:
    """
    Dependency to get the current user from the access token.
    Raises HTTPException if the token is invalid or expired.
    """
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload['user_id']