from .test_app import *


def test_regsiter_user(client: FlaskClient) -> None:
    data = dict(
        EMAIL='user@example.com',
        USERNAME='example',
        PASSWORD='tester',
        GENDER='M',
        FIRST_NAME='uno',
        LAST_NAME='dos',
    )

    rv = register_user(client, **data)
    json = rv.get_json()
    assert json['message']


def test_login_logout(client: FlaskClient) -> None:
    username = 'tester'
    password = 'tester'

    rv = login(client, username, password)
    json = rv.get_json()

    assert json['userId']