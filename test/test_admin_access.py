from .test_app import *


def test_admin_access(client: FlaskClient) -> None:

    rv = client.get('/admin/user')
    assert b'Redirecting' in rv.data