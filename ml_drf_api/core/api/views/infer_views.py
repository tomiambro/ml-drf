import logging
from pathlib import Path

import joblib
from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from ml_drf_api.core.api.serializers import InferSerializer
from ml_drf_api.core.tasks import log_model_output

model_path = Path(settings.APPS_DIR / "ml/saved_models/randomforest_breast_cancer.pkl")


# Disable atomic transactions so we can log validation errors
@method_decorator(transaction.non_atomic_requests, name="dispatch")
class InferView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = InferSerializer

    def post(self, request):
        serializer = InferSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                estimator = joblib.load(model_path)
                input = serializer.validated_data["input"]
                try:
                    prediction = estimator.predict([input])[0]
                    # log the output to the db using a celery task
                    log_model_output.delay(input=str(input), output=str(prediction))
                    payload = {
                        "message": f"This is the model's prediction: {prediction}"
                    }
                except Exception as e:
                    logging.warn(f"The following exception occured: {e}")
                    log_model_output.delay(input=str(input), error=e)
                    raise e
        except ValidationError as e:
            log_model_output.delay(input="", error=e.detail)
            logging.warn(f"Wrong input provided: {e}")
            raise e

        return Response(payload)
