"""
Module for Vote class model
"""

from sqlalchemy.types import Integer, String, Boolean, TIMESTAMP
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, func
from datetime import datetime, timezone

from .base import Base


class Vote(Base):
    """Vote model"""

    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (PrimaryKeyConstraint("user_id", "post_id"),)
