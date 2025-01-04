"""
Module for User class model
"""

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Integer, String, Boolean, TIMESTAMP
from sqlalchemy import Column, ForeignKey, func
from datetime import datetime, timezone

from models.post import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
