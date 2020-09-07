import pytest
from celery.result import EagerResult

from hisitter.users.tasks import send_confirmation_email
from hisitter.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """A basic test to execute the get_users_count Celery task."""
    UserFactory.create_batch(3)
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = send_confirmation_email.delay()
    assert isinstance(task_result, EagerResult)
    assert task_result.result == 3
