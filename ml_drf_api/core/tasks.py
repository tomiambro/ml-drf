import logging

from celery import current_app as app
from django.db import IntegrityError

from ml_drf_api.core.models import ModelLog


@app.task()
def log_model_output(input: str, output: str, error: str = ""):
    try:
        ModelLog.objects.create(input=input, output=output, error_log=error)
    except IntegrityError as e:
        logging.info(f"There was an error: {e}")
