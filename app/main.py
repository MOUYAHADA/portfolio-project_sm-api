from fastapi import FastAPI
from routes import posts
from database import DB

app = FastAPI()

app.include_router(posts.router)

db = DB()
if db._session is None:
  print("Not connected")
else:
  print("Connected")

new_user = db.create_user('med22', 'med@medd.com', 'asdfasdfdsdsaf')

print(new_user.email)