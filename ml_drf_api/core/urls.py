from django.urls import path

from .api.views import InferView

urlpatterns = [
    path("infer", InferView.as_view(), name="infer"),
]
