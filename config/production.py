import os
from .default import *

ENV = os.getenv('FLAS_ENV')
SECRET_KEY = os.urandom(24)
JWT_SECRET_KEY = os.urandom(24)

TESTING = False
DEBUG = False
TESTING = False
