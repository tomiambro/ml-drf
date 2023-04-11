# from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class TestCoreView:
    def test_infer_view(self, user_client):
        url = reverse("infer")
        response = user_client.get(url)
        assert response.json()["message"] == "This is the model's prediction:"
