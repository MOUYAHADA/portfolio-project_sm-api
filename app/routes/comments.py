#!/usr/bin/env python3
"""
Module for comments route
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from schemas import CommentCreate, CommentDisplay
from models import Comment, User, Post
from database import get_db
from oauth2 import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post(
    "/", response_model=CommentDisplay, status_code=status.HTTP_201_CREATED
)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a comment for a post"""
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    new_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=current_user.id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{post_id}", response_model=list[CommentDisplay])
def get_comments_for_post(post_id: int, db: Session = Depends(get_db)):
    """Retrieve all comments for a specific post"""
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments


@router.put("/{comment_id}", response_model=CommentDisplay)
def update_comment(
    comment_id: int,
    updated_comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment",
        )

    comment.content = updated_comment.content
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}
