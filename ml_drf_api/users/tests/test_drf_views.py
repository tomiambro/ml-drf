import pytest
from django import test
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ml_drf_api.users.api.views import UserViewSet
from ml_drf_api.users.models import User
from ml_drf_api.users.tests.factories import UserFactory


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }

    def test_list_users(self, auth_user_client):
        UserFactory()
        url = reverse("api:user-list")
        response = auth_user_client.get(url)

        assert response.status_code == 200, response.json()
        assert len(response.json()) == 1

    def test_delete_user(self, user):
        # User 2 tries to delete another user
        user_2 = UserFactory()
        client = test.Client()
        client.force_login(user_2)
        url = reverse("api:user-detail", kwargs={"username": user.username})

        response = client.delete(url)
        assert response.status_code == 404, response.json()
        # Assert original user still exists
        assert User.objects.filter(username=user.username).exists()

    def test_register(self, unauth_user_client):
        url = reverse("api:user-register")
        data = {"username": "test", "password": "test"}

        # Delete test user before registering
        User.objects.filter(username="test").delete()
        assert not User.objects.filter(username="test").exists()

        response = unauth_user_client.post(url, data)
        assert response.status_code == 201, response.json()
        assert User.objects.filter(username="test").exists()

    def test_register_existing_user(self, unauth_user_client):
        url = reverse("api:user-register")
        data = {"username": "test", "password": "test"}

        # Delete test user before registering
        User.objects.filter(username="test").delete()
        assert not User.objects.filter(username="test").exists()

        unauth_user_client.post(url, data)
        response = unauth_user_client.post(url, data)
        assert response.status_code == 400, response.json()
        assert response.json() == {
            "username": ["A user with that username already exists."]
        }
