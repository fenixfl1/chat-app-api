from flask import Flask
from .ext import socketio, jwt, adm, migrate, sql, cors, ma, sess
from .admin.admin import MyAdminIndexView
from app.requests import *
from app import events


def create_app(settings_module=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(settings_module)

    from .auth import bp_auth
    app.register_blueprint(bp_auth)

    from .admin import bp_adm
    app.register_blueprint(bp_adm)

    jwt.init_app(app)
    adm.init_app(app)
    sql.init_app(app)
    migrate.init_app(app, sql)
    cors.init_app(app)
    ma.init_app(app)
    sess.init_app(app)
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ORIGINS'])

    app.before_request(load_user)
    app.teardown_request(teardown_request)

    return app
