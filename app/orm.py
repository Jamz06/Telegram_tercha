# %%
from typing import Optional, List
import datetime

from sqlalchemy import Column, Integer, String,  create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
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
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120))
    t_chat_id: Mapped[str] = mapped_column(String(120))
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]]
    level: Mapped[Optional[int]]
    admin: Mapped[Optional[int]]

    dogs: Mapped[List["Dog"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, t_chat_id, username, first_name, last_name):
        self.t_chat_id = t_chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f"""\nИмя: {self.first_name}\nФамилия: {self.last_name}\nСобаки: {self.dogs}"""

class Dog(Base):
    '''
        Класс собаки пользователя
    '''
    __tablename__ = 'dogs'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    t_user: Mapped[int] = mapped_column(ForeignKey("t_user.id"))
    user: Mapped["User"] = relationship(back_populates="dogs")

    def __init__(self, name, t_user):
        self.name = name
        self.t_user = t_user

    def __repr__(self) -> str:
        return self.name

class Sport(Base):
    '''
        Виды спорта
    '''
    __tablename__ = 'sport'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    
    card_types: Mapped[List["CardType"]] = relationship(
        back_populates="sport_t", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return self.name

class CardType(Base):
    '''
        Виды карточек
    '''
    __tablename__ = 'card_type'
    card_type: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    dificulty: Mapped[Optional[int]]
    sport: Mapped[int] = mapped_column(ForeignKey("sport.id"))

    sport_t: Mapped["Sport"] = relationship(back_populates="card_types")

    def __repr__(self) -> str:
        return self.name

class Card(Base):
    '''
        Карточка
    '''
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(250))
    points: Mapped[str] = mapped_column(String(250))
    card_type: Mapped[int] = mapped_column(ForeignKey("card_type.card_type"))

    def __repr__(self) -> str:
        return self.name
    

class Tasks(Base):
    '''
        Карточка
    '''
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    dog: Mapped[int] = mapped_column(ForeignKey("dogs.id"))
    card: Mapped[int] = mapped_column(ForeignKey("card.id"))
    video_id: Mapped[str] = mapped_column(String(200))
    pic_id: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(String(255))
    result: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime())
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime())
    status: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    who_rated: Mapped[int] = mapped_column(ForeignKey("user.id"))
    rate: Mapped[Optional[int]]

class Statuses(Base):
    '''
        Статусы заданий
    '''
    __tablename__ = 'task_status'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    task_closed: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return self.name

# ---------------------------------------------------------------------------- #
# %%
if __name__ == '__main__':

    foo = session.query(CardType).filter_by(name='Зеленая')
    pass
# %%
