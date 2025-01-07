from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


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


# Post Schemas
class PostCreate(BaseModel):
    """Schema for creating a post"""

    title: str
    content: str
    owner_id: int
    published: bool = False


class PostDisplay(BaseModel):
    """Schema for displaying a post"""

    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime
    owner: UserDisplay

    class Config:
        from_attributes = True


# Comment Schemas
class CommentCreate(BaseModel):
    """Schema for creating a comment"""

    content: str


class CommentDisplay(CommentCreate):
    """Schema for displaying a comment"""

    id: int
    owner_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime


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


# Token Schema
class TokenData(BaseModel):
    """Schema for the token payload"""

    id: int | None = None
