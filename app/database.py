from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

class DB:
  def __init__(self):
    self.engine = create_engine(settings.db_url)
    self.__session = None
    
  @property
  def _session(self):
    if self.__session is None:
      DBsession = sessionmaker(bind=self.engine)
      self.__session = DBsession()
    return self.__session

