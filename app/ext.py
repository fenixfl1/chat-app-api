from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

socketio = SocketIO()
login = LoginManager()
jwt = JWTManager()
