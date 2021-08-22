from app import create_app as application
from app.ext import socketio
from app.database import init_db
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = application(settings_module)

with app.app_context():
    init_db()


if __name__ == '__main__':
    socketio.run(app)
