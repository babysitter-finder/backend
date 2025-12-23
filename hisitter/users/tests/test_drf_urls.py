import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_users_list():
    assert reverse("users:users-list") == "/users/"
    assert resolve("/users/").view_name == "users:users-list"


def test_users_detail(user):
    url = reverse("users:users-detail", kwargs={"username": user.username})
    assert url == f"/users/{user.username}/"
    assert resolve(url).view_name == "users:users-detail"
