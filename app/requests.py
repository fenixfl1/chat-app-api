from .globals import current_user
from .database import db
from .database.models import User
from .utils.callbacks import load_user_callback


def teardown_request(exception=None):

    db.remove()
    return exception


def load_user():
    if isinstance(current_user, User):
        print(current_user.is_authenticated)

        load_user_callback()