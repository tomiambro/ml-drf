from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

# from django.shortcuts import render


def infer(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    else:
        payload = {"message": "This is the model's prediction:"}
        return JsonResponse(payload)
