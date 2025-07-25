from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/menu/', views.MenuItemListView.as_view(), name='menu-api'),
]