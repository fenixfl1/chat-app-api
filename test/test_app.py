from types import GeneratorType
import pytest, os, tempfile
from werkzeug.test import TestResponse
from app import create_app
from app.database import init_db
from flask import json
from flask.testing import FlaskClient


@pytest.fixture
def client() -> 'GeneratorType[FlaskClient]':
    testing_settingS = os.getenv('APP_TESTING_SETTINGS')
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(testing_settingS)

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def register_user(client: FlaskClient, **kwargs) -> TestResponse:
    return client.post('/register_user',
                       data=json.dumps({
                           'EMAIL': kwargs.get('EMAIL'),
                           'USERNAME': kwargs.get('USERNAME'),
                           'PASSWORD': kwargs.get('PASSWORD'),
                           'GENDER': kwargs.get('GENDER'),
                           'FIRST_NAME': kwargs.get('FIRST_NAME'),
                           'LAST_NAME': kwargs.get('LAST_NAME')
                       }),
                       headers={"Content-Type": "application/json"},
                       follow_redirects=True)


def login(client: FlaskClient, username: str, password: str) -> TestResponse:
    return client.post('/login',
                       data=json.dumps({
                           'USERNAME': username,
                           'PASSWORD': password
                       }),
                       headers={"Content-Type": "application/json"},
                       follow_redirects=True)


def logout(client: FlaskClient) -> TestResponse:
    return client.get('/logout', follow_redirects=True)
