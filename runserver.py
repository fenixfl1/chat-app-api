from app import create_app as application
from app.ext import socketio
import os

settings_module = os.getenv('APP_SETTINGS_MODULE')

app = application(settings_module)


if __name__ == '__main__':
    socketio.run(app)
