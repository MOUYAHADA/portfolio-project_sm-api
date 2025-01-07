#!/usr/bin/env python
"""
Module for user authentication route
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db, DB
from utils import verify_password
from oauth2 import create_access_token
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), db: DB = Depends(get_db)
):
    """
    Authenticate a user and return a JWT token.
    """
    try:
        # Fetch user using the database class
        user = db.find_user(username=user_credentials.username)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # Create JWT token
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
