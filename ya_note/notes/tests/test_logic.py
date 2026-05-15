from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base import BaseTestCase


class TestNoteCreation(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form_data = {
            'title': 'Новое название',
            'text': 'Новый текст',
            'slug': 'new_slug',
        }

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        notes_count = Note.objects.count()

        response = self.author_client.post(
            self.add_url,
            data=self.form_data,
        )

        self.assertRedirects(
            response,
            self.success_url,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count + 1,
        )

        new_note = Note.objects.get()

        params = (
            (new_note.title, self.form_data['title']),
            (new_note.text, self.form_data['text']),
            (new_note.slug, self.form_data['slug']),
            (new_note.author, self.author),
        )

        for result, expected in params:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    def test_anon_user_cannot_create_note(self):
        notes_count = Note.objects.count()

        response = self.client.post(
            self.add_url,
            data=self.form_data,
        )

        expected_url = (
            f'{self.login_url}?next={self.add_url}'
        )

        self.assertRedirects(
            response,
            expected_url,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count,
        )

    def test_empty_slug(self):
        Note.objects.all().delete()
        notes_count = Note.objects.count()

        form_data = {
            'title': 'Новое название',
            'text': 'Новый текст',
        }

        response = self.author_client.post(
            self.add_url,
            data=form_data,
        )

        self.assertRedirects(
            response,
            self.success_url,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count + 1,
        )

        new_note = Note.objects.get()

        expected_slug = slugify(
            form_data['title'],
        )

        self.assertEqual(
            new_note.slug,
            expected_slug,
        )

    def test_not_unique_slug(self):
        notes_count = Note.objects.count()

        form_data = {
            'title': 'Другая заметка',
            'text': 'Текст',
            'slug': self.note.slug,
        }

        response = self.author_client.post(
            self.add_url,
            data=form_data,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count,
        )

        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )

        self.assertFormError(
            response.context['form'],
            'slug',
            errors=self.note.slug + WARNING,
        )


class TestNoteEditDelete(BaseTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.form_data = {
            'title': 'Новое название',
            'text': 'Новый текст',
            'slug': 'new_slug',
        }

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_url,
            data=self.form_data,
        )

        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
        )

        self.assertRedirects(
            response,
            self.success_url,
        )

        updated_note = Note.objects.get(
            id=self.note.id,
        )

        params = (
            (
                updated_note.title,
                self.form_data['title'],
            ),
            (
                updated_note.text,
                self.form_data['text'],
            ),
            (
                updated_note.slug,
                self.form_data['slug'],
            ),
            (
                updated_note.author,
                self.note.author,
            ),
        )

        for result, expected in params:
            with self.subTest(result=result):
                self.assertEqual(result, expected)

    def test_other_user_cannot_edit_note(self):
        response = self.reader_client.post(
            self.edit_url,
            data=self.form_data,
        )

        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
        )

        note_from_db = Note.objects.get(
            id=self.note.id,
        )

        params = (
            (
                self.note.title,
                note_from_db.title,
            ),
            (
                self.note.text,
                note_from_db.text,
            ),
            (
                self.note.slug,
                note_from_db.slug,
            ),
            (
                self.note.author,
                note_from_db.author,
            ),
        )

        for expected, result in params:
            with self.subTest(result=result):
                self.assertEqual(expected, result)

    def test_author_can_delete_note(self):
        notes_count = Note.objects.count()

        response = self.author_client.post(
            self.delete_url,
        )

        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
        )

        self.assertRedirects(
            response,
            self.success_url,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count - 1,
        )

    def test_other_user_cant_delete_note(self):
        notes_count = Note.objects.count()

        response = self.reader_client.post(
            self.delete_url,
        )

        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
        )

        self.assertEqual(
            Note.objects.count(),
            notes_count,
        )
