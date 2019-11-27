import pytest

from users.models import CustomUser


@pytest.mark.django_db
def test_user_create():
    CustomUser.objects.create_user('john')
    assert CustomUser.objects.count() == 1
