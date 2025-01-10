#!/usr/bin/python3
"""
Module for posts route
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.exc import NoResultFound
from typing import List

from app.schemas import PostCreate, PostDisplay, PostDisplayAll
from app.database import get_db, DB
from app.models import User
from app.oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostDisplay])
def get_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(10, gt=0, description="Number of posts to fetch"),
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """View all posts"""
    posts = db.get_posts(skip, limit)
    return posts

@router.get("/{post_id}", response_model=PostDisplayAll)
def get_posts(
    post_id: int,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """View all posts"""
    try:
        post = db.find_post_with_id(id=post_id)
        return post
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post doesn't exist"
        )


@router.post("/", response_model=PostDisplayAll)
def create_post(
    post: PostCreate,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new post"""
    data = post.model_dump()
    data["owner_id"] = current_user.id
    new_post = db.create_post(**data)
    return new_post


@router.put("/{id}", response_model=PostDisplayAll)
def update_post(
    id: int,
    post: PostCreate,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing post"""
    try:
        old_post = db.find_post_with_id(id=id)
        if old_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this post",
            )
        data = post.model_dump()
        new_post = db.update_post(post_id=id, **data)
        return new_post
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post doesn't exist"
        )


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(
    post_id: int,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a post"""
    try:
        post = db.find_post_with_id(id=post_id)
        if current_user.id != post.owner_id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify/delete this post",
            )
        db._session.delete(post)
        db._session.commit()
        return {"detail": "Post deleted successfully"}
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
