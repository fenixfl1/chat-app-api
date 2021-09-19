from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_session import Session

socketio = SocketIO()
jwt = JWTManager()
adm = Admin()
migrate = Migrate()
sql = SQLAlchemy()
cors = CORS()
ma = Marshmallow()
sess = Session()