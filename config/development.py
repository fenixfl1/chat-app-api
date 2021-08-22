import os
from .default import *

ENV = os.getenv('FLASK_ENV')
SECRET_KEY = os.urandom(24)
JWT_SECRET_KEY = os.urandom(24)

SESSION_COOKIE_DOMAIN = 'localhost'

TESTING = True
DEBUG = True
