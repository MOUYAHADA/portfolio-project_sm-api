from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import get_db, DB, NoResultFound
from schemas import UserCreate, UserDisplay, UserPassword
from typing import List, Any

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: DB = Depends(get_db)):
    users = db.get_all_users(limit=10)
    return users


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


@router.put("/{user_id}")
def update_user_password(
    user_id: int, password: UserPassword, db: DB = Depends(get_db)
):
    try:
        db.update_user_password(user_id, password=password.password)
        return {"message": "Successfully updated"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist"
        )


@router.delete("/{user_id}")
def delete_user(user_id: int, db: DB = Depends(get_db)):
    """Delete a user"""
    try:
        user = db.find_user(id=user_id)
        db._session.delete(user)
        db._session.commit()
        return Response(content="User deleted successfully", status_code=200)

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' was not found",
        )
