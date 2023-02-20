from sqlalchemy import Column, Integer, String, BOOLEAN, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

db_uri = environ.get('DB_URI', False) 
if not db_uri:
    exit(1)
# TODO: передавать db_uri из стартового файла
engine = create_engine(db_uri, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# При работе с орм импортировать session и классы таблиц
session = Session()

# -------------------------- ОПИСАНИЕ КЛАССОВ ТАБЛИЦ ------------------------- #
class User(Base):
    '''
        Класс пользователя в ТГ
    '''
    __tablename__ = 't_user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    t_chat_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    level = Column(Integer)
    admin = Column(BOOLEAN)

    def __init__(self, t_chat_id, username, first_name, last_name):
        self.t_chat_id = t_chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


# ---------------------------------------------------------------------------- #

