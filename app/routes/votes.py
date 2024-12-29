from fastapi import APIRouter

router = APIRouter(
  prefix="/votes",
  tags=["Votes"]
)

@router.get('/')
def get_votes():
  return {"votes": []}