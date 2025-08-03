
from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^devices/?.*', views.gimme, name='devices'),
    re_path('^prefixes/?.*', views.gimme, name='prefixes'),
    re_path('^vlans/?.*', views.gimme, name='vlans'),
    re_path('^ip_addresses/?.*', views.gimme, name='ip_addresses'),
    re_path('^object_changes/?.*', views.gimme),
]