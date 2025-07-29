from django.urls import path, include, re_path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customers, name='customers'),
    path('health', views.health, name='health'),
    path('menu', views.menu_items, name='menu'),
    re_path('^(dcim|ipam)/',include('infrasot.urls'))
]