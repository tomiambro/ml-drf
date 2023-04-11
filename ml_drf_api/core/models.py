from django.db import models
from model_utils.models import TimeStampedModel


class ModelLog(TimeStampedModel):
    input = models.CharField(max_length=300, null=False)
    output = models.CharField(max_length=100, null=True)
    error_log = models.CharField(max_length=200, null=True)
