from pathlib import Path

import joblib
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from .tasks import log_model_output

model_path = Path(settings.APPS_DIR / "ml/saved_models/randomforest_breast_cancer.pkl")


def infer(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    else:
        estimator = joblib.load(model_path)
        input = request.POST.getlist("input")
        try:
            prediction = estimator.predict([input])[0]
            log_model_output.delay(input=str(input), output=str(prediction))
        except ValueError as e:
            log_model_output.delay(input=str(input), output=str(prediction), error=e)
            raise e

        payload = {"message": f"This is the model's prediction: {prediction}"}
        return JsonResponse(payload)
