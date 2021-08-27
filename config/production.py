import os
from .default import *

ENV = os.getenv('APP_ENV')
SECRET_KEY = os.urandom(24)
JWT_SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = os.getenv('JAWSDB_URL')

TESTING = False
DEBUG = FAlseTESTING = False
