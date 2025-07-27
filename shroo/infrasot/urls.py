
from django.contrib import admin
from django.urls import path, include  # include is used to bring in app URLs
from . import views

urlpatterns = [
    path('devices', views.get_devices, name='devices'),
]