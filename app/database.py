from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from config import settings
from models import User, Post, Base
from utils import hash_password


class DB:
    """Database class"""

    def __init__(self):
        """Initialize DB"""
        db_url = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.__session = None

    @property
    def _session(self):
        """Create session"""
        if self.__session is None:
            DBsession = sessionmaker(bind=self.engine)
            self.__session = DBsession()
        return self.__session

    def get_all_users(self, limit: int = 10):
        """Get all posts"""
        users = self._session.query(User).limit(limit).all()
        return users

    def find_user(self, **kwargs) -> User:
        """Find a user using their username"""
        for key, value in kwargs.items():
            if key in {'id', 'username', 'email'}:
              result = self._session.query(User).filter(getattr(User, key) == value).one()
              if result is not None:
                  return result
        raise NoResultFound

    def find_user_with_email(self, email: str) -> User:
        """Find a user using their email"""
        if email:
            result = self._session.query(User).filter(User.email == email).one()
            if result is None:
                raise NoResultFound
            return result
        raise ValueError("email argument was not given")

    def get_all_posts(self, limit: int = 0):
        """Get all posts"""
        posts = self._session.query(Post).limit(limit).all()
        return posts

    def find_post_with_id(self, id: str):
        """Find an existing post using its id
        """
        post = self._session.query(Post).filter_by(id=id).first()
        if post is None:
            raise NoResultFound
        return post

    def create_post(
        self, title: str, content: str, owner_id: int, published: bool = False
    ):
        """Create a new post"""
        if title and content:
            new_post = Post()
            new_post.title = title
            new_post.content = content
            new_post.owner_id = owner_id
            self._session.add(new_post)
            self._session.commit()
            return new_post
        
    def update_post(self, post_id: int, **kwargs):
        """Update an existing post"""
        post = self.find_post_with_id(id=post_id)
        for key, value in kwargs.items():
            if not hasattr(post, key):
                self._session.rollback()
                raise ValueError(f"Post object has no attribute named {key}")
            else:
                setattr(post, key, value)
        
        self._session.commit()
        return post

    def create_user(self, username: str, email: str, password: str):
        """Create a new user
        """
        if username and email and password:
            try:
                self.find_user(email=email)
                raise ValueError(f"User with email {email} already exists")
            except NoResultFound:
                pass
            try:
                self.find_user(username=username)
                raise ValueError(f"User with username {username} already exists")
            except NoResultFound:
                pass

            new_user = User()
            new_user.username = username
            new_user.hashed_password = hash_password(password)
            new_user.email = email

            self._session.add(new_user)
            self._session.commit()

            return new_user

    def update_user_password(self, user_id: int, password: str):
        """Update a user
        """
        user = self._session.query(User).filter_by(id=user_id).one()
        if user is None:
            raise NoResultFound
        
        user.hashed_password = hash_password(password)
        self._session.commit()


def get_db():
    db = DB()
    try:
        yield db
    finally:
        db._session.close()