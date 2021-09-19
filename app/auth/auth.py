from datetime import datetime, timedelta
from flask import jsonify, request, current_app, session
from app.database.models import User
from app.database.schemas import UserSchema
from app.database import db
from app.utils.callbacks import load_user_callback
from app.globals import current_user
from . import bp_auth
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity)


@bp_auth.post('/login')
def login():

    data = request.get_json()

    username: str = data.get('USERNAME')
    password: str = data.get('PASSWORD')

    user = User.get_by_email(username) or User.get_by_username(username)

    if not user:
        return jsonify({"errorMessage": "User not found."})

    elif (user.check_password_hash(password) and user.IS_ACTIVE):
        current_date = datetime.now()
        session_age = timedelta(minutes=3)
        expires_delta = current_date + session_age

        access_token = create_access_token(user.USER_ID,
                                           expires_delta=timedelta(seconds=3))

        user.refresh_login_info('login')

        session['user_id'] = user.USER_ID
        load_user_callback()

        return jsonify({
            'userId': user.USER_ID,
            'username': user.USERNAME,
            'email': user.EMAIL,
            'sessionCookie': {
                'token': access_token,
                'expiration': expires_delta.isoformat()
            }
        })
    else:
        return jsonify({"errorMessage": "Incorrect username or password."})


@bp_auth.get('/logout')
@jwt_required()
def logout():
    user = User.get_by_id(get_jwt_identity())
    user.refresh_login_info('logout')
    return jsonify({"msg": "logout"})


@bp_auth.post('/register_user')
def create_user():
    DATA_REQUIRED: dict = [
        'EMAIL', 'PASSWORD', 'FIRST_NAME', 'LAST_NAME', 'GENDER'
    ]

    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data received."})

        for i in range(len(DATA_REQUIRED)):
            if DATA_REQUIRED[i] not in data:
                return jsonify({"message": f"{DATA_REQUIRED[i]} is required"})

        if User.get_by_email(data.get('EMAIL')):
            return jsonify(
                {"message": f"{data.get('EMAIL')} is already in use."})

        new_user = User(**data)

        db.add(new_user)
        db.commit()
        return jsonify({"msg": "User created successfully."})

    except Exception as e:
        return jsonify({"message": f"{e}"})


@bp_auth.get('/get_users_info')
def get_users_info() -> jsonify:

    # if current_user.is_authenticated:

    users = User.query.all()
    users_schema = UserSchema(many=True)

    return users_schema.dumps(users)


@bp_auth.get('/room/<int:ROOM_ID>')
def Rooms():
    return 'Hi'