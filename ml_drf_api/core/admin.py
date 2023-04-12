from django.contrib import admin

from .models import ModelLog


@admin.register(ModelLog)
class ModelLogAdmin(admin.ModelAdmin):
    list_display = ("id", "output", "error_log")
