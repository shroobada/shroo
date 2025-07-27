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


def get_devices_streaming_view(request):
    assert nb is not None
    def generate():
        for chunk in nb.get_data_streaming_sync("devices", chunk_size=50):
            yield json.dumps(chunk) + '\n'

    response = StreamingHttpResponse(generate())
    print(response)
    return response