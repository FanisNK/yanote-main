from notes.forms import NoteForm
from .base import BaseTestCase


class TestContent(BaseTestCase):

    def test_notes_list_for_different_users(self):
        test_data = (
            (self.author_client, True),
            (self.reader_client, False),
        )

        for client, note_in_list in test_data:
            with self.subTest(
                client=client,
                note_in_list=note_in_list,
            ):
                response = client.get(self.list_url)
                object_list = response.context['object_list']

                self.assertEqual(
                    self.note in object_list,
                    note_in_list,
                )

    def test_pages_contains_form(self):
        urls = (
            self.add_url,
            self.edit_url,
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)

                self.assertIn(
                    'form',
                    response.context,
                )
                self.assertIsInstance(
                    response.context['form'],
                    NoteForm,
                )
