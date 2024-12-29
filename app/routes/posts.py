from fastapi import APIRouter

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

@router.get('/')
def get_posts():
  return {"posts": []}