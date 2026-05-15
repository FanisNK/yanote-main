from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create(username='Admin')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def admin_client(admin):
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='New title',
        text='New text',
    )


@pytest.fixture
def all_news():
    today = datetime.today()

    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='New comment text',
    )


@pytest.fixture
def comments(author, news):
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Text {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


FORM_DATA = {
    'text': 'New form comment text',
}
