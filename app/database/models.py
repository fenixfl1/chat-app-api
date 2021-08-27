from werkzeug.security import (generate_password_hash, check_password_hash)
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    CHAR,
)
from . import Base, engine
from datetime import datetime
from flask import request


class User(Base):
    __tablename__ = 'USERS'

    ID = Column(Integer, primary_key=True)
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
    IS_ACTIVE = Column(Boolean, default=True)
    IS_ADMIN = Column(Boolean, default=False)

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

    def refresh_login_info(self) -> None:
        engine.execute(f"""
            UPDATE USERS SET LOGIN_COUNT = '{self.LOGIN_COUNT + 1}',
            CURRENT_LOGIN_IP = '{request.remote_addr}',
            CURRENT_LOGIN_AT = '{datetime.now()}',
            LAST_LOGIN_AT = '{datetime.now()}'
            WHERE ID = '{self.ID}'
        """)

    def reresh_logout_info(self):
        engine.execute(f"""
            UPDATE USERS SET LAST_LOGIN_AT = {None},
            CURRENT_LOGIN_IP = '{None}'
            WHERE ID = {self.ID}          
        """)

    def set_password(self, password: str) -> str:
        return generate_password_hash(f'{password}')

    def check_password_hash(self, password: str) -> bool:
        return check_password_hash(self.PASSWORD, password)
