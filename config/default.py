import os
from os.path import abspath, dirname
from dotenv import load_dotenv

APP_ROOT = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = os.getenv('JAWSDB_URL')
SQLALCHEMY_TRACK_MODIFICATION = False

DEBUG = False
TESTING = False
ENV = ''
