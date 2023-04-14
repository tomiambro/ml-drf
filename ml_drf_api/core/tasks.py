import logging

from celery import Task
from celery import current_app as app
from django.db import IntegrityError
from django.utils import timezone

from ml_drf_api.core.models import ModelLog


class BaseLogTask(Task):
    soft_time_limit = 60 * 15  # in seconds, 15 minutes
    time_limit = soft_time_limit + 30  # in seconds, 15.5 minutes
    ignore_result = False

    def before_start(self, task_id, args, kwargs):
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # Celery uses confusing function signatures...
        # If the task succeeds the arguments are as expected.
        # If the task fails the error is in the retval and the einfo parameter is empty.
        if not isinstance(retval, Exception):
            log = ModelLog.objects.get(id=retval)
            log.status = status
            log.completed_at = timezone.now()
            log.celery_task_uuid = task_id
            log.save()


@app.task(base=BaseLogTask)
def log_model_output(input: str, output: str = "", error: str = ""):
    try:
        log = ModelLog.objects.create(input=input, output=output, error_log=error)
        return log.id
    except IntegrityError as e:
        logging.info(f"There was an error: {e}")
