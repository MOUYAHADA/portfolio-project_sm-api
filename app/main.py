from fastapi import FastAPI
from app.routes import posts

app = FastAPI()

app.include_router(posts.router)