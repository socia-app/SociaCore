import uuid  # For generating unique token ID
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from app.core.config import settings
from app.utils.datetime import get_current_time
from app.models.auth import AccessToken, RefreshToken, TokenModel

ALGORITHM = "HS256"

def get_jwt_payload(token: str) -> TokenModel:
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print('payload ', payload)
        # Create and return a TokenModel instance with the decoded payload
        return TokenModel(sub=payload.get("sub"), exp=payload.get("exp"))

    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token validation failed: {str(e)}"
        )

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> AccessToken:
    if expires_delta:
        expire = get_current_time() + expires_delta
    else:
        expire = get_current_time() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    jti = str(uuid.uuid4())
    to_encode = {"exp": expire, "sub": str(subject), "jti": jti}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Create an instance of AccessToken with the encoded JWT and expiration time
    access_token = AccessToken(
        token=encoded_jwt,
        expires_at=expire,
        token_type="Bearer"
    )

    return access_token

def create_refresh_token(subject: str) -> RefreshToken:
    expire = get_current_time() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    to_encode = {"sub": str(subject), "exp": expire, "jti": jti}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    # Create an instance of RefreshToken with the encoded JWT and expiration time
    refresh_token = RefreshToken(
        token=encoded_jwt,
        expires_at=expire
    )

    return refresh_token
