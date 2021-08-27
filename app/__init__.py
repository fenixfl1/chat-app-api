from flask import Flask
from .ext import socketio, jwt, adm, migrate, sql
from .admin.admin import MyAdminIndexView


def create_app(settings_module: str) -> Flask:
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
    socketio.init_app(app, cors_allowed_origins="*")

    return app
