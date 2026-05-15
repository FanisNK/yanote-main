from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testAuthor')
        cls.reader = User.objects.create(username='testReader')

        cls.note = Note.objects.create(
            title='Название заметки',
            text='Текст заметки',
            slug='test-slug',
            author=cls.author,
        )

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.home_url = reverse('notes:home')
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')

        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')

        cls.detail_url = reverse(
            'notes:detail',
            args=(cls.note.slug,),
        )

        cls.edit_url = reverse(
            'notes:edit',
            args=(cls.note.slug,),
        )

        cls.delete_url = reverse(
            'notes:delete',
            args=(cls.note.slug,),
        )
