from flask import Flask
from .ext import socketio, jwt


def create_app(settings_module: str) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

    if app.config.get('TESTING', True):
        print(" * Running in development mode")
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=True)
    else:
        print(" * Running in production mode")
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=True)

    from .auth import bp_auth
    app.register_blueprint(bp_auth)

    jwt.init_app(app)
    # add async_mode='eventlet' in socketio instance as parameter to use eventlet, but you need to install them fisrt
    socketio.init_app(app, cors_allowed_origins="*")

    return app
