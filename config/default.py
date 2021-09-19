from datetime import timedelta
import os
from os.path import abspath, dirname
from dotenv import load_dotenv

APP_ROOT = dirname(dirname(abspath(__file__)))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CORS_HEADERS = 'Content-Type'
CORS_ORIGINS = os.getenv('CORS_ORIGIN')

SESSION_TYPE = 'sqlalchemy'
# PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)

DEBUG = False
TESTING = False
ENV = ''
