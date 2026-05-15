from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

COMMENT_TEXT = 'New comment text'
UPDATED_COMMENT_TEXT = 'Updated text'


def test_anonymous_user_cannot_create_comment(
    client,
    detail_url,
):
    comments_count = Comment.objects.count()
    response = client.post(detail_url, data={'text': COMMENT_TEXT})

    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == comments_count


def test_user_can_create_comment(
    author_client,
    author,
    news,
    detail_url,
):
    Comment.objects.all().delete()
    comments_count = Comment.objects.count()

    response = author_client.post(
        detail_url,
        data={'text': COMMENT_TEXT},
    )

    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == comments_count + 1

    comment = Comment.objects.get()

    assert comment.text == COMMENT_TEXT
    assert comment.author == author
    assert comment.news == news


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cannot_use_bad_words(
    author_client,
    detail_url,
    bad_word,
):
    comments_count = Comment.objects.count()

    response = author_client.post(
        detail_url,
        data={'text': f'Text {bad_word} text'},
    )

    assert Comment.objects.count() == comments_count

    assertFormError(
        response.context['form'],
        'text',
        errors=WARNING,
    )


def test_author_can_delete_comment(
    author_client,
    delete_url,
    detail_url,
    comment,
):
    comments_count = Comment.objects.count()

    response = author_client.delete(delete_url)

    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, f'{detail_url}#comments')

    assert Comment.objects.count() == comments_count - 1
    assert not Comment.objects.filter(id=comment.id).exists()


def test_user_cannot_delete_comment_of_another_user(
    admin_client,
    delete_url,
    comment,
):
    comments_count = Comment.objects.count()

    response = admin_client.delete(delete_url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count

    current_comment = Comment.objects.get(id=comment.id)

    assert current_comment.text == comment.text
    assert current_comment.author == comment.author
    assert current_comment.news == comment.news


def test_author_can_edit_comment(
    author_client,
    edit_url,
    detail_url,
    comment,
):
    response = author_client.post(
        edit_url,
        data={'text': UPDATED_COMMENT_TEXT},
    )

    assert response.status_code == HTTPStatus.FOUND
    assertRedirects(response, f'{detail_url}#comments')

    updated_comment = Comment.objects.get(id=comment.id)

    assert updated_comment.text == UPDATED_COMMENT_TEXT
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


def test_user_cannot_edit_comment_of_another_user(
    admin_client,
    edit_url,
    comment,
):
    response = admin_client.post(
        edit_url,
        data={'text': UPDATED_COMMENT_TEXT},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    current_comment = Comment.objects.get(id=comment.id)

    assert current_comment.text == comment.text
    assert current_comment.author == comment.author
    assert current_comment.news == comment.news
