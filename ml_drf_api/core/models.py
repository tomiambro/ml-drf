from celery import states
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

ALL_STATES = sorted(states.ALL_STATES)
TASK_STATE_CHOICES = sorted(zip(ALL_STATES, ALL_STATES))


class ModelLog(TimeStampedModel):
    input = models.CharField(max_length=300, null=False, editable=False)
    output = models.CharField(max_length=100, null=True, editable=False)
    error_log = models.CharField(max_length=200, null=True, editable=False)
    description = models.CharField(max_length=500, null=True)
    status = models.CharField(
        max_length=50,
        default=states.PENDING,
        choices=TASK_STATE_CHOICES,
        verbose_name=_("Task State"),
        help_text=_("Current state of the task being run"),
        editable=False,
    )
    completed_at = models.DateTimeField(
        null=True,
        verbose_name=_("Completed DateTime"),
        help_text=_("Datetime field when the task was completed in UTC"),
    )
    celery_task_uuid = models.UUIDField(null=True, editable=False)

    def __str__(self) -> str:
        return f"Model log #{self.id}"
