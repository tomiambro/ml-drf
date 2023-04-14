import pytest
from celery import states
from django.urls import reverse

from .models import ModelLog
from .tasks import log_model_output

pytestmark = [pytest.mark.django_db(transaction=True)]

data = {
    "input": [
        17.99,
        10.38,
        122.8,
        1001,
        0.1184,
        0.2776,
        0.3001,
        0.1471,
        0.2419,
        0.07871,
        1.095,
        0.9053,
        8.589,
        153.4,
        0.006399,
        0.04904,
        0.05373,
        0.01587,
        0.03003,
        0.006193,
        25.38,
        17.33,
        184.6,
        2019,
        0.1622,
        0.6656,
        0.7119,
        0.2654,
        0.4601,
        0.1189,
    ]
}


class TestCoreView:
    def test_infer_view_auth(self, auth_user_client):
        url = reverse("infer")
        response = auth_user_client.post(url, data)
        assert response.json()["message"] == "This is the model's prediction: 1"
        assert response.status_code == 200

    def test_infer_view_auth_no_input(self, auth_user_client):
        url = reverse("infer")
        data = {}
        response = auth_user_client.post(url, data)
        assert response.json() == {"input": ["This field is required."]}
        assert response.status_code == 400

    def test_infer_view_unauth(self, unauth_user_client):
        url = reverse("infer")
        response = unauth_user_client.post(url, data)
        assert response.status_code == 403

    def test_log_model_output(self):
        log_model_output.delay(input=data["input"], output="1")
        logs = ModelLog.objects.all()
        assert len(logs) == 1

        log = logs.first()
        assert log.status == states.SUCCESS
        assert log.error_log == ""

    def test_log_integration(self, auth_user_client):
        url = reverse("infer")
        response = auth_user_client.post(url, data)
        logs = ModelLog.objects.all()

        assert response.status_code == 200, response.json()
        assert len(logs) == 1

    def test_log_integration_validation_error(self, auth_user_client):
        url = reverse("infer")
        data = {"input": []}
        response = auth_user_client.post(url, data)
        logs = ModelLog.objects.all()
        log = logs.first()

        assert response.status_code == 400, response.json()
        assert len(logs) == 1
        assert log.error_log == "{'input': ['This field is required.']}"

    def test_log_integration_value_error(self, auth_user_client):
        url = reverse("infer")
        data = {"input": [0]}
        response = auth_user_client.post(url, data)
        logs = ModelLog.objects.all()
        log = logs.first()

        assert response.status_code == 200, response.json()
        assert len(logs) == 1
        assert (
            "RandomForestClassifier is expecting 30 features as input." in log.error_log
        )
