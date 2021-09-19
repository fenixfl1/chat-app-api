from sqlalchemy.orm import backref, relationship
from werkzeug.security import (generate_password_hash, check_password_hash)
from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    CHAR,
    ForeignKey,
)
from . import Base, engine
from datetime import datetime
from flask import request


class User(Base):
    __tablename__ = 'USERS'

    USER_ID = Column(Integer, primary_key=True)
    EMAIL = Column(String(100), nullable=False, unique=True)
    USERNAME = Column(String(20), nullable=False, unique=True)
    FIRST_NAME = Column(String(50))
    LAST_NAME = Column(String(50))
    GENDER = Column(CHAR)
    PASSWORD = Column(String(255), nullable=False)
    CIUNTRY = Column(String(5))
    LAST_LOGIN_AT = Column(DateTime(timezone=True))
    CURRENT_LOGIN_AT = Column(DateTime(timezone=True))
    CURRENT_LOGIN_IP = Column(String(100))
    LOGIN_COUNT = Column(Integer, default=0)
    IS_ACTIVE = Column(Boolean(), default=True)
    IS_ADMIN = Column(Boolean(), default=False)
    CREATED_AT = Column(DateTime(timezone=True),
                        nullable=False,
                        default=func.now())
    MESSAGES = relationship('Messages', back_populates='USER')
    ROOMS = relationship('Rooms',
                         secondary='USERS_ROOMS',
                         backref=backref('USERS', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.EMAIL = kwargs.get('EMAIL')
        self.USERNAME = kwargs.get('USERNAME')
        self.FIRST_NAME = kwargs.get('FIRST_NAME')
        self.LAST_NAME = kwargs.get('LAST_NAME')
        self.GENDER = kwargs.get('GENDER')
        self.IS_ADMIN = kwargs.get('IS_ADMIN')
        self.PASSWORD = self.set_password(kwargs.get('PASSWORD'))

    def __repr__(self):
        return f'{self.FIRST_NAME}'

    @staticmethod
    def get_by_email(email: str) -> 'User':
        return User.query.filter_by(EMAIL=email).first()

    @staticmethod
    def get_by_username(username: str) -> 'User':
        return User.query.filter_by(USERNAME=username).first()

    @staticmethod
    def get_by_id(id: int) -> 'User':
        return User.query.get(id)

    @property
    def is_authenticated(self):
        return True

    def refresh_login_info(self, action: str) -> None:
        query = ''
        if action == 'login':
            query = f"""
                UPDATE USERS SET LOGIN_COUNT = '{self.LOGIN_COUNT + 1}',
                CURRENT_LOGIN_IP = '{request.remote_addr}',
                CURRENT_LOGIN_AT = '{datetime.now()}',
                LAST_LOGIN_AT = '{datetime.now()}'
                WHERE USER_ID = '{self.USER_ID}'
            """
        else:
            query = f"""
                UPDATE USERS SET LAST_LOGIN_AT = {None},
                CURRENT_LOGIN_IP = '{None}'
                WHERE USER_ID = {self.USER_ID}          
            """

        engine.execute(query)

    def set_password(self, password: str) -> str:
        return generate_password_hash(f'{password}')

    def check_password_hash(self, password: str) -> bool:
        return check_password_hash(self.PASSWORD, password)


class UsersRoom(Base):
    __tablename__ = 'USERS_ROOMS'

    USERS_ROOM_ID = Column(Integer(), primary_key=True)
    USER_ID = Column(Integer(), ForeignKey('USERS.USER_ID'))
    ROOM_ID = Column(Integer(), ForeignKey('ROOMS.ROOM_ID'))


class Rooms(Base):
    __tablename__ = 'ROOMS'

    ROOM_ID = Column(Integer(), primary_key=True)
    ROOM_NAME = Column(String(50), nullable=False)
    DESCRIPTION = Column(String(150))
    ROOM_TYPE = Column(CHAR(), nullable=False)
    ROOM_CODE = Column(String(15), unique=True)
    MESSAGES = relationship('Messages', back_populates='ROOM')
    CREATED_AT = Column(DateTime(timezone=True),
                        nullable=False,
                        default=func.now())
    IS_ACTIVE = Column(Boolean(), nullable=False, default=True)

    def __init__(self, **kwargs):
        self.ROOM_NAME = kwargs.get('ROOM_NAME')
        self.DESCRIPTION = kwargs.get('DESCRIPTION')
        self.ROOM_TYPE = kwargs.get('ROOM_TYPE')
        self.ROOM_CODE = kwargs.get('ROOM_CODE')

    def __repr__(self):
        return f'{self.ROOM_NAME}'

    @staticmethod
    def find_room(**kwargs):
        return Rooms.query.filter(**kwargs).all()


class Messages(Base):
    __tablename__ = 'MESSAGES'

    MESSAGE_ID = Column(Integer(), primary_key=True)
    USER_ID = Column(Integer, ForeignKey('USERS.USER_ID', ondelete='CASCADE'))
    USER = relationship('User', back_populates='MESSAGES')
    ROOM_ID = Column(Integer, ForeignKey('ROOMS.ROOM_ID', ondelete='CASCADE'))
    ROOM = relationship('Rooms', back_populates='MESSAGES')
    MESSAGE = Column(String(250), nullable=False)
    MESSAGE_TYPE = Column(CHAR(), nullable=False, default='T')
    MESSAGE_STATE = Column(Boolean(), nullable=False, default=False)
    SENT_AT = Column(DateTime(timezone=True),
                     nullable=False,
                     default=func.now())

    def __repr__(self):
        return f'{self.MESSAGE}'


class Sessions(Base):
    __tablename__ = 'SESSIONS'

    id = Column(Integer(), primary_key=True)
    session_id = Column(String(100))
    data = Column(String(100))
    expiry = Column(String(10))

    def __repr__(self):
        return f'{self.session_id}'