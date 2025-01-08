#!/usr/bin/env python3
"""
Module for users route
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List, Any

from database import get_db, DB, NoResultFound
from schemas import UserCreate, UserDisplay, UserPassword, UserDisplayWithPosts
from oauth2 import get_current_user
from models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: DB = Depends(get_db)):
    users = db.get_all_users(limit=10)
    return users


@router.get("/me", response_model=UserDisplayWithPosts)
def get_one_user(
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=UserDisplay)
def get_one_user(user_id: int, db: DB = Depends(get_db)):
    try:
        user = db.find_user(id=user_id)
        return user
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/", response_model=UserDisplay)
def create_user(new_user: UserCreate, db: DB = Depends(get_db)):
    data = new_user.model_dump()
    try:
        user = db.create_user(**data)
    except ValueError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="User with email/username already exists",
        )
    return user


@router.post("/me")
def update_user_password(
    pw: UserPassword,
    db: DB = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        db.update_user_password(user_id=current_user.id, password=pw.password)
        return {"message": "Successfully updated"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )


@router.delete("/me")
def delete_user(
    db: DB = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a user"""
    try:
        user = db.find_user(id=current_user.id)
        db._session.delete(user)
        db._session.commit()
        return Response(content="User deleted successfully", status_code=200)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found or already deleted",
        )
