from fastapi import FastAPI
from routes import posts, users, votes

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)