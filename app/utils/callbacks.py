from flask import _request_ctx_stack, session, current_app
from app.database.models import User


def load_user_callback() -> 'None':

    user = User()
    user_id: id = session.get('user_id')

    if user_id:
        print(f'{user_id:*^80}')
        user = User.get_by_id(user_id)
        setattr(_request_ctx_stack.top, 'user', user)