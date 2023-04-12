from django.contrib import admin

from .models import ModelLog


@admin.register(ModelLog)
class ModelLogAdmin(admin.ModelAdmin):
    list_display = ("name", "output", "error_log")
    readonly_fields = ("input", "output", "error_log")

    def name(self, obj):
        return obj.__str__()
