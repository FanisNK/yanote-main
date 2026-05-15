from http import HTTPStatus

from .base import BaseTestCase


class TestRoutes(BaseTestCase):

    def test_pages_availability(self):
        test_data = (
            (self.client, self.home_url, HTTPStatus.OK),
            (self.client, self.login_url, HTTPStatus.OK),
            (self.client, self.signup_url, HTTPStatus.OK),

            (
                self.author_client,
                self.list_url,
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                self.add_url,
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                self.success_url,
                HTTPStatus.OK,
            ),

            (
                self.author_client,
                self.detail_url,
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                self.edit_url,
                HTTPStatus.OK,
            ),
            (
                self.author_client,
                self.delete_url,
                HTTPStatus.OK,
            ),

            (
                self.reader_client,
                self.detail_url,
                HTTPStatus.NOT_FOUND,
            ),
            (
                self.reader_client,
                self.edit_url,
                HTTPStatus.NOT_FOUND,
            ),
            (
                self.reader_client,
                self.delete_url,
                HTTPStatus.NOT_FOUND,
            ),
        )

        for client, url, status in test_data:
            with self.subTest(url=url, status=status):
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_logout_page_availability(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )

    def test_redirects_for_anonymous_client(self):
        urls = (
            self.detail_url,
            self.edit_url,
            self.delete_url,
            self.add_url,
            self.success_url,
            self.list_url,
        )

        for url in urls:
            with self.subTest(url=url):
                redirect_url = (
                    f'{self.login_url}?next={url}'
                )

                response = self.client.get(url)

                self.assertRedirects(
                    response,
                    redirect_url,
                )
