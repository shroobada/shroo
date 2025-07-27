from django.urls import path, include
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('customers', views.customers, name='customers'),
    path('menu', views.menu_items, name='menu'),
    path('dcim/',include('infrasot.urls'))
]