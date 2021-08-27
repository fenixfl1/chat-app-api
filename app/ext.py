from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
jwt = JWTManager()
adm = Admin()
migrate = Migrate()
sql = SQLAlchemy()
