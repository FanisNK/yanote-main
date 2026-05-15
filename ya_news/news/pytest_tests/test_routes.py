from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture as lf
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url_fixture, parametrized_client, expected_status',
    (
        ('home_url', lf('client'), OK),
        ('detail_url', lf('client'), OK),
        ('login_url', lf('client'), OK),
        ('signup_url', lf('client'), OK),
        ('edit_url', lf('author_client'), OK),
        ('delete_url', lf('author_client'), OK),
        ('edit_url', lf('admin_client'), NOT_FOUND),
        ('delete_url', lf('admin_client'), NOT_FOUND),
    ),
)
def test_pages_availability(
    request,
    url_fixture,
    parametrized_client,
    expected_status,
):
    url = request.getfixturevalue(url_fixture)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


def test_logout_availability(logout_url, client):
    response = client.post(logout_url)
    assert response.status_code == OK


@pytest.mark.parametrize(
    'url_fixture',
    ('edit_url', 'delete_url'),
)
def test_redirect_for_anonymous_client(
    request,
    client,
    login_url,
    url_fixture,
):
    url = request.getfixturevalue(url_fixture)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
