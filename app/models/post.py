"""
Module for Post class model
"""

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Integer, String, Boolean, TIMESTAMP
from sqlalchemy import Column, ForeignKey, func
from datetime import datetime, timezone

Base = declarative_base()


class Post(Base):
    """Post model"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='FALSE')
    
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', back_populates=True)
