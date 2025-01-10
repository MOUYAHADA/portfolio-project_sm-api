#!/usr/bin/env python3
"""
Module for pydantic schemas
"""
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import List


# User Schemas
class UserCreate(BaseModel):
    """Schema for creating a user"""

    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    """Schema for displaying a user"""

    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserPassword(BaseModel):
    """Schema for user password"""

    password: str


# Vote Schemas
class VoteCreate(BaseModel):
    """Schema for creating a vote"""

    post_id: int
    dir: conint(strict=True, ge=0, le=1)  # 1 = Upvote, 0 = Remove vote


class VoteDisplay(BaseModel):
    """Schema for displaying a vote"""

    user: UserDisplay
    post_id: int
    created_at: datetime


# Post Schemas
class PostCreate(BaseModel):
    """Schema for creating a post"""

    title: str
    content: str
    published: bool = False


class PostDisplayMin(BaseModel):
    """Schema for displaying a post"""

    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class PostDisplay(PostDisplayMin):
    """Schema for displaying a post"""

    published: bool
    owner_id: int


class PostDisplayAll(PostDisplay):
    """Schema for displaying a post"""

    created_at: datetime
    updated_at: datetime
    owner: UserDisplay
    votes: List[VoteDisplay]


# Comment Schemas
class CommentCreate(BaseModel):
    """Schema for creating a comment"""

    content: str
    post_id: int

    class Config:
        from_attributes = True


class CommentDisplay(CommentCreate):
    """Schema for displaying a comment"""

    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


# Token Schema
class TokenData(BaseModel):
    """Schema for the token payload"""

    id: int | None = None


class UserDisplayWithPosts(UserDisplay):
    """Schema for displaying a user and their posts"""

    posts: List[PostDisplayMin]
