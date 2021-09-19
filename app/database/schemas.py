from app.ext import ma
from .models import User, Rooms
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema

user_object = [
    "IS_ACTIVE", "LOGIN_COUNT", "LAST_NAME", "CURRENT_LOGIN_IP", "CREATED_AT",
    "IS_ADMIN", "EMAIL", "CURRENT_LOGIN_AT", "USERNAME", "FIRST_NAME",
    "GENDER", "CIUNTRY", "USER_ID", "LAST_LOGIN_AT"
]


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User

    ROOMS = ma.List(ma.HyperlinkRelated('bp_auth.Rooms', url_key='ROOM_ID'))
    for field in user_object:
        field = ma.auto_field


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rooms
        include_relationships = True
        load_instance = True

    USERS = ma.List(ma.HyperlinkRelated('USERS'))
