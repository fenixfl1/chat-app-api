from datetime import datetime
from flask import jsonify, request
from flask.helpers import make_response
from app.database.models import User
from app.database import db
from . import bp_auth
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity)


@bp_auth.after_request
def after_request(response):
    origin = request.headers.get('Origin')

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    return response


@bp_auth.post('/login')
def login():

    data = request.get_json()

    username: str = data['EMAIL']
    password: str = data['PASSWORD']

    user = User.get_by_email(username)

    if not user:
        return jsonify({"message": "User not found."})
    else:
        if (user.check_password_hash(password) and user.IS_ACTIVE):
            access_token = create_access_token(user.ID, expires_delta=None)

            user.refresh_login_info()

            return jsonify({
                'user_id': user.ID,
                'username': f'{user.FIRST_NAME} {user.LAST_NAME}',
                'email': user.EMAIL,
                'sessionCookie': {
                    'token': access_token,
                    'expiration': None
                }
            })
        else:
            return jsonify({"message": "Incorrect username or password."})


@bp_auth.get('/logout')
@jwt_required()
def logout():
    user = User.get_by_id(get_jwt_identity())
    user.reresh_logout_info()
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
