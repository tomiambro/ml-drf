from django import test
from django.http.response import HttpResponseForbidden
from django.urls import reverse


class TestCoreView:
    def test_infer_view_auth(self, user_client):
        url = reverse("infer")
        response = user_client.get(url)
        assert response.json()["message"] == "This is the model's prediction:"
        assert response.status_code == 200

    def test_infer_view_unauth(self, user):
        url = reverse("infer")
        client = test.Client()
        response = client.get(url)
        assert isinstance(response, HttpResponseForbidden)
        assert response.status_code == 403
