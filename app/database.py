from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from config import settings
from models.user import User
from models.post import Post


class DB:
    """Database class"""

    def __init__(self):
        """Initialize DB"""
        from models.base import Base  
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

    def find_user_with_username(self, username: str):
        """Find a user using their username"""
        if username:
            result = self._session.query(User).filter(
              User.username == username
            ).one()
            if result is None:
                raise NoResultFound
            return result
        raise ValueError("username argument was not given")

    def find_user_with_email(self, email: str):
        """Find a user using their email"""
        if email:
            result = self._session.query(User).filter(User.email == email).one()
            if result is None:
                raise NoResultFound
            return result
        raise ValueError("email argument was not given")

    def create_post(self, title: str, content: str, owner_id: int, published: bool = False):
        """Create a new post"""
        if title and content:
            new_post = Post()
            new_post.title = title
            new_post.content = content
            new_post.owner_id = owner_id
            self._session.add(new_post)
            self._session.commit()

    def create_user(self, username: str, email: str, hashed_password: str):
        if username and email and hashed_password:
            try:
                self.find_user_with_email(email=email)
                raise ValueError(f"User with email {email} already exists")
            except NoResultFound:
                pass
            try:
                self.find_user_with_username(username=username)
                raise ValueError(f"User with username {username} already exists")
            except NoResultFound:
                pass

            new_user = User()
            new_user.username = username
            new_user.hashed_password = hashed_password
            new_user.email = email

            self._session.add(new_user)
            self._session.commit()

            return new_user
