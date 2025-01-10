#!/usr/bin/env python3
"""
Module for votes route
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import VoteCreate
from app.models import User, Vote
from app.database import get_db, DB
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteCreate,
    db: DB = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the post exists
    post = db.find_post_with_id(id=vote.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    # Check if the vote already exists
    existing_vote = (
        db._session.query(Vote)
        .filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
        .first()
    )
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already voted for this post",
            )
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db._session.add(new_vote)
        db._session.commit()
        return {"message": "Vote added successfully"}
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist",
            )
        db._session.delete(existing_vote)
        db._session.commit()
        return {"message": "Vote removed successfully"}
