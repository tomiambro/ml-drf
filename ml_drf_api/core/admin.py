from django.contrib import admin

from .models import ModelLog


@admin.register(ModelLog)
class ModelLogAdmin(admin.ModelAdmin):
    list_display = ("name", "output", "error_log", "description")
    readonly_fields = ("input", "output", "error_log", "status")

    def name(self, obj):
        return obj.__str__()
