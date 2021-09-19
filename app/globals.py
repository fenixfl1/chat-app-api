from app.utils.callbacks import load_user_callback
from werkzeug.local import LocalProxy
from .database.models import User
from flask import has_request_context, _request_ctx_stack

current_user: User = LocalProxy(lambda: _get_user())


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        load_user_callback()
    return getattr(_request_ctx_stack.top, 'user', None)