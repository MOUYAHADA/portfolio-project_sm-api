# Social Media Application API

This is a **social media application** built using **FastAPI**. It supports features like user authentication, creating and managing posts, voting, and comments. The project is designed as a demonstration of building RESTful APIs with FastAPI.

---

## Features

- **User Authentication**: 
  - Secure login with JWT tokens.
  - Create, update, and deleting users.

- **Post Management**: 
  - Create, update, delete, and view posts.
  - Search for posts with keywords.

- **Voting System**: 
  - Upvote or downvote posts.

- **Comments**: 
  - Add, edit, and delete comments on posts.

---

## Technologies Used

- **Backend**: 
  - FastAPI: For creating APIs.
  - SQLAlchemy: For database ORM.
  - Pydantic: For data validation.

- **Database**: 
  - SQLite (can be switched to other databases like PostgreSQL).

- **Authentication**: 
  - JWT (JSON Web Tokens).

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MOUYAHADA/portfolio-project_sm-api.git
   cd fastapi-social-media
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python database_setup.py
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

### **Auth**

- **Login**: `POST /auth/login`
- **Register**: `POST /auth/register`

### **Users**

- **Get All Users**: `GET /users`
- **Get User by ID**: `GET /users/{id}`

### **Posts**

- **Create Post**: `POST /posts`
- **Get Posts**: `GET /posts`
- **Search Posts**: `GET /posts/search`
- **Update Post**: `PUT /posts/{id}`
- **Delete Post**: `DELETE /posts/{post_id}`

### **Votes**

- **Vote on a Post**: `POST /votes`

### **Comments**

- **Add Comment**: `POST /comments`
- **Edit Comment**: `PUT /comments/{id}`
- **Delete Comment**: `DELETE /comments/{id}`

---

## Folder Structure

```
app/
├── routes/         # Contains route files (posts, users, auth, votes, comments)
├── schemas.py      # Pydantic models for validation
├── models.py       # SQLAlchemy models for database
├── database.py     # Database connection and queries
├── oauth2.py       # JWT authentication utilities
├── main.py         # Main FastAPI app
tests/
    ├── test_auth.py        # Tests for authentication
    ├── test_posts.py       # Tests for posts
    ├── test_votes.py       # Tests for voting
    └── test_comments.py    # Tests for comments
```

---

## Future Improvements

- Add support for file uploads (e.g., images for posts).
- Implement notifications for votes and comments.
- Improve testing coverage.
- Add WebSocket support for real-time updates.

---

## Contributing

Feel free to submit issues and pull requests to improve this project. 

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

Special thanks to the FastAPI and SQLAlchemy communities for their extensive documentation and examples.
```

---

### Next Steps
- Replace placeholder information (e.g., GitHub URL) with your actual data.
- If you want, I can also create a minimal version of this README or add custom sections based on your preferences. Let me know!