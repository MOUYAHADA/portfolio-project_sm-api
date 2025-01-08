#!/usr/bin/env python3
"""
Main FastAPI app module
"""
from fastapi import FastAPI
from routes import posts, users, votes, auth, comments

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
app.include_router(comments.router)
app.include_router(auth.router)