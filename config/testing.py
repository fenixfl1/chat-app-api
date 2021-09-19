import tempfile

db_fd, db_path = tempfile.mkstemp()

CORS_ORIGINS = '*'
SECRET_KEY = 'testing'

DEBUG = False
TESTING = True
ENV = 'testing'

SQLALCHEMY_DATABASE_URI = db_path
SQLALCHEMY_TRACK_MODIFICATIONS = False