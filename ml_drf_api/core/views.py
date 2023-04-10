from django.http import Http404, JsonResponse

# from django.shortcuts import render


def infer(request):
    if request.user.is_authenticated:
        payload = {"message": "This is the model's prediction:"}
        return JsonResponse(payload)
    else:
        raise Http404
