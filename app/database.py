from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from config import settings
from models import post, user, vote


class DB:
    """Database class"""

    def __init__(self):
        """Initialize DB"""
        db_url = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
        self.engine = create_engine(db_url)
        post.Base.metadata.create_all(bind=self.engine)
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
            result = self._session.query(
                user.User, user.User.username == username
            ).one()
            if result is None:
                raise NoResultFound
            return result
        raise ValueError("username argument was not given")

    def find_user_with_email(self, email: str):
        """Find a user using their email"""
        if email:
            result = self._session.query(user.User, user.User.email == email).one()
            if result is None:
                raise NoResultFound
            return result
        raise ValueError("email argument was not given")

    def create_post(self, title: str, content: str, published: bool = False):
        """Create a new post"""
        if title and content:
            new_post = post.Post()
            new_post.title = title
            new_post.content = content
            self._session.add(new_post)
            self._session.commit()

    def create_user(self, username: str, email: str, hashed_password: str):
        if username and email and hashed_password:
            new_user = user.User()
            new_user.username = username
            new_user.hashed_password = hashed_password
            self._session.add(new_user)
            self._session.commit()

