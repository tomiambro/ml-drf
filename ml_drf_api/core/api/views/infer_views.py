from pathlib import Path

import joblib
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ml_drf_api.core.api.serializers import InferSerializer
from ml_drf_api.core.tasks import log_model_output

model_path = Path(settings.APPS_DIR / "ml/saved_models/randomforest_breast_cancer.pkl")


class InferView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = InferSerializer(data=request.data)
        payload = {"message": "No input provided"}
        if serializer.is_valid():
            estimator = joblib.load(model_path)
            input = serializer.validated_data["input"]
            try:
                prediction = estimator.predict([input])[0]
                # log the output to the db using a celery task
                log_model_output.delay(input=str(input), output=str(prediction))
                payload = {"message": f"This is the model's prediction: {prediction}"}
            except ValueError as e:
                payload = {"message": f"{e}"}
                log_model_output.delay(input=str(input), error=e)
                raise e
        return Response(payload)
