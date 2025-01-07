from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import DB
from database import get_db
from schemas import PostCreate, PostDisplay
from sqlalchemy.exc import NoResultFound
from datetime import datetime, timezone


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/")
def get_posts(limit: int = 10, db: DB = Depends(get_db)):
    """View all posts"""
    posts = db.get_posts(limit)
    return posts


@router.get("/search")
def get_posts(query: str, limit: int = 10, db: DB = Depends(get_db)):
    """Search for posts"""
    posts = db.get_posts(limit, search=query)
    return posts


@router.post("/", response_model=PostDisplay)
def create_post(post: PostCreate, db: DB = Depends(get_db)):
    """Create a new post"""
    data = post.model_dump()
    new_post = db.create_post(**data)
    return new_post


@router.put("/{id}", response_model=PostDisplay)
def update_post(id: int, post: PostCreate, db: DB = Depends(get_db)):
    """Update an existing post"""
    try:
        data = post.model_dump()
        new_post = db.update_post(post_id=id, **data)
        return new_post
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post doesn't exist"
        )


@router.delete("/{post_id}", response_model=PostDisplay)
def delete_post(post_id: int, db: DB = Depends(get_db)):
    """Update an existing post"""
    try:
        post = db.find_post_with_id(id=post_id)
        db._session.delete(post)
        db._session.commit()
        return Response(
            content="Post deleted successfully",
            status_code=status.HTTP_202_ACCEPTED
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post doesn't exist"
        )
