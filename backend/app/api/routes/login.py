import hashlib
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from app.utils.datetime import get_current_time
from app.api.deps import SessionDep, get_current_user
from app.core.security import (  # Adjust the import based on your structure
    create_access_token,
    create_refresh_token,
    get_jwt_payload,
)
from app.models.auth import OtplessToken, RefreshTokenPayload, UserAuthResponse
from app.models.user import UserBusiness, UserPublic  # Import your UserPublic model

router = APIRouter()


def generate_number_from_string(s):
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % 10 ** 8


@router.post("/verify_token/business", response_model=UserAuthResponse)
async def business_user_google_login(request: OtplessToken, session: SessionDep):
    try:
        # Verify the Google token with Google
        # token_info_url = "https://oauth2.googleapis.com/tokeninfo"
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"{token_info_url}?id_token={request.google_token}")

        # if response.status_code != 200:
        #     raise HTTPException(status_code=400, detail="Invalid Google token")

        # # Parse user info
        # user_info = response.json()
        # email = user_info.get("email")
        # user_id = user_info.get("sub")  # Google user ID

        # Check for user by Google ID or email
        email = request.otpless_token+ "test@gmail.com"   # Replace this with the actual email from the SDK response
        user = session.query(UserBusiness).filter(UserBusiness.email == email).first()

        if not user:
            # Create new user if not found
            user = UserBusiness(
                email=email,
                is_active=True
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        # Create tokens
        access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(subject=str(user.id))

        # Store refresh token
        user.refresh_token = refresh_token.token
        session.add(user)
        session.commit()

        return UserAuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            issued_at=datetime.now(timezone.utc)
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify_token/public", response_model=UserAuthResponse)
async def verify_token(request: OtplessToken, session: SessionDep):
    try:
        # Verify the token using OTPLess SDK
        # Uncomment and implement token verification with OTPLess
        # user_details = OTPLessAuthSDK.UserDetail.verify_token(
        #     request.otpless_token,
        #     settings.CLIENT_ID,
        #     settings.CLIENT_SECRET
        # )

        # Simulated user details for demonstration
        # phone_number = "8130181469"  # Replace this with the actual phone number from the SDK response
        phone_number = str(generate_number_from_string(request.otpless_token))

        # Check for the user by phone number
        user = session.query(UserPublic).filter(UserPublic.phone_number == phone_number).first()

        if not user:
            # Create a new user if not found
            user = UserPublic(
                phone_number=phone_number,
                is_active=True
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        # Create tokens
        access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=30))
        refresh_token = create_refresh_token(subject=str(user.id))

        # Store the new refresh token in the user's record
        user.refresh_token = refresh_token.token
        session.add(user)  # Add the updated user to the session
        session.commit()  # Commit the changes to the database

        return UserAuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            issued_at=get_current_time()
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh_token", response_model=UserAuthResponse)
async def refresh_token(request: RefreshTokenPayload, session: SessionDep):
    try:
        # Decode and validate the refresh token payload
        payload = get_jwt_payload(request.refresh_token)

        # Extract the user ID (sub) from the payload
        user_id = payload.sub

        # Fetch the user from the database using the user ID
        user = (
            session.query(UserPublic)
            .filter(UserPublic.id == user_id)
            .first()
        ) or (
            session.query(UserBusiness)
            .filter(UserBusiness.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify if the refresh token in the database matches the provided token
        if user.refresh_token != request.refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Check if the token has expired
        current_time = get_current_time()
        if payload.exp and datetime.fromtimestamp(payload.exp, timezone.utc) < current_time:
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # If valid, generate new tokens
        new_access_token = create_access_token(subject=user_id, expires_delta=timedelta(minutes=30))
        new_refresh_token = create_refresh_token(subject=user_id)

        # Update the user's refresh token in the database
        user.refresh_token = new_refresh_token.token
        session.add(user)
        session.commit()

        # Return the new tokens and issue time
        return UserAuthResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            issued_at=current_time
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logout")
async def logout(
    session: SessionDep,
    current_user: Annotated[UserPublic | UserBusiness, Depends(get_current_user)]):
    try:
        # Invalidate the refresh token by setting it to None or an empty string
        current_user.refresh_token = None
        session.add(current_user)
        session.commit()

        return {"message": "Logout successful, refresh token invalidated"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
