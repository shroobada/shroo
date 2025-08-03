import json
from pprint import pprint

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from .apps import nb


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_devices(request):
    assert nb is not None
    devices = nb.get_data_sync(request.path[1:].replace('/', '.'))
    return JsonResponse({"devices": devices})

def get_count(request):
    assert nb is not None
    print('request:',request.path[1:].replace('/', '.'))
    count=nb.get_data_sync(request.path[1:].replace('/', '.'))

    return JsonResponse({"count": count})

def gimme(request,*args, **kwargs):
    assert nb is not None
    result=nb.get_data_sync(request.path[1:].replace('/', '.').rstrip('.'))
    return JsonResponse(result, safe=False)
