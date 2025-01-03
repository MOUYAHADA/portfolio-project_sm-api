"""
Module for Vote class model
"""

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Integer, String, Boolean, TIMESTAMP
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from datetime import datetime, timezone

from app.models.post import Base


class Vote(Base):
    """Vote model"""

    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (PrimaryKeyConstraint("user_id", "post_id"),)
