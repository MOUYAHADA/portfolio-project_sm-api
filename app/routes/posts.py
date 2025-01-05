from fastapi import APIRouter, Depends
from database import DB
from database import get_db
from schemas import PostCreate, PostDisplay
from sqlalchemy.exc import NoResultFound
from datetime import datetime, timezone

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

@router.get('/')
def get_posts(db: DB = Depends(get_db)):
  """View all posts
  """
  posts = db.get_all_posts(limit=10)
  return posts

@router.post('/', response_model=PostDisplay)
def create_post(post: PostCreate, db: DB = Depends(get_db)):
  """Create a new post
  """
  data = post.model_dump()
  new_post = db.create_post(**data)
  return new_post

@router.put('/{id}', response_model=PostDisplay)
def update_post(id: int, post: PostCreate, db: DB = Depends(get_db)):
  """Update an existing post
  """
  try:
    data = post.model_dump()
    new_post = db.update_post(post_id=id, **data)
    return new_post
  except NoResultFound:
    return {"message": "NOT FOUND"}