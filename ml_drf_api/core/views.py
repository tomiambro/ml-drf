from pathlib import Path

import joblib
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

model_path = Path(settings.APPS_DIR / "ml/saved_models/randomforest_breast_cancer.pkl")


def infer(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    else:
        estimator = joblib.load(model_path)
        prediction = estimator.predict([request.POST.getlist("input")])

        payload = {"message": f"This is the model's prediction: {prediction[0]}"}
        return JsonResponse(payload)
