import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from ml_drf_api.users.api.views import UserViewSet
from ml_drf_api.users.models import User


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
