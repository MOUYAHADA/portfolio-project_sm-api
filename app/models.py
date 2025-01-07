from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Post(Base):
    """Post model"""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="FALSE")

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    votes = relationship("Vote", back_populates="post", cascade="all, delete")


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")
    votes = relationship("Vote", back_populates="user", cascade="all, delete")


class Vote(Base):
    """Vote model"""

    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")

    __table_args__ = (PrimaryKeyConstraint("user_id", "post_id"),)


class Comment(Base):
    """Comment model"""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
