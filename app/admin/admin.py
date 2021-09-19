from . import bp_adm
from app.ext import adm
from app.database import db
from app.database.models import Messages, Rooms, User
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import current_user, jwt_required
from flask import redirect, url_for, jsonify
from flask_admin import AdminIndexView, expose


class AdminView(ModelView):
    # create_modal = True
    # edit_modal = True
    can_view_details = True

    # @jwt_required()
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('bp_adm.inaccessible'))


class UserView(AdminView):
    column_searchable_list = ('USERNAME', 'EMAIL', 'FIRST_NAME', 'LAST_NAME')
    column_filters = ('USERNAME', 'FIRST_NAME')

    column_exclude_list = ['PASSWORD']


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @jwt_required
    def index(self):
        return self.render('index.html.j2', name='Chat App Admin')


@bp_adm.get('/')
@jwt_required()
def inaccessible():
    return jsonify({"message": "This isn't the way to access this url."})


adm.add_view(UserView(User, db))
adm.add_view(AdminView(Rooms, db))
adm.add_view(AdminView(Messages, db))
