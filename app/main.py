# from fastapi import FastAPI
# from app.routes import posts

# app = FastAPI()

# app.include_router(posts.router)
from database import DB

db = DB()
if db._session is None:
  print("Not connected")
else:
  print("Connected")