#!/usr/bin/env python3
"""
Module for comments route
"""
from fastapi import APIRouter, HTTPException, Depends, status

from app.schemas import CommentCreate, CommentDisplay
from app.models import Comment, User, Post
from app.database import get_db, DB, NoResultFound
from app.oauth2 import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/", response_model=CommentDisplay, status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: CommentCreate,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a comment for a post"""
    try:
        post = db.find_post_with_id(id=comment.post_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    new_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        owner_id=current_user.id,
    )
    db._session.add(new_comment)
    db._session.commit()
    db._session.refresh(new_comment)
    return new_comment


@router.get("/{post_id}", response_model=list[CommentDisplay])
def get_comments_for_post(post_id: int, db: DB = Depends(get_db)):
    """Retrieve all comments for a specific post"""
    comments = db._session.query(Comment).filter(Comment.post_id == post_id).all()
    return comments


@router.put("/{comment_id}", response_model=CommentDisplay)
def update_comment(
    comment_id: int,
    updated_comment: CommentCreate,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a comment"""
    comment = (
        db._session.query(Comment).filter(Comment.id == comment_id).first()
    )
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment",
        )

    comment.content = updated_comment.content
    db._session.commit()
    db._session.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a comment"""
    comment = db._session.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if comment.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )

    db._session.delete(comment)
    db._session.commit()
    return {"detail": "Comment deleted successfully"}
