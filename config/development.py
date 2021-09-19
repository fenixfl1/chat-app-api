import os
from .default import *

ENV = os.getenv('FLASK_ENV')
SECRET_KEY = os.urandom(24)
JWT_SECRET_KEY = os.urandom(24)

SESSION_IN_USER = None

TESTING = True
DEBUG = True