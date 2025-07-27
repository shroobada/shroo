import importlib

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.apps import apps

from shroo.settings import LOCAL_APPS
from .models import MenuItem
from .serializers import MenuItemSerializer
import json
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponse


def index(request):
    # Get menu items for display
    menu_items = MenuItem.objects.filter(parent=None, is_active=True)
    serializer = MenuItemSerializer(menu_items, many=True)

    # Calculate stats
    total_subitems = MenuItem.objects.filter(parent__isnull=False, is_active=True).count()
    active_items = MenuItem.objects.filter(is_active=True).count()

    # Format JSON for pretty display
    menu_json = json.dumps(serializer.data, indent=2, ensure_ascii=False)

    context = {
        'menu_items': menu_items,
        'menu_json': menu_json,
        'total_subitems': total_subitems,
        'active_items': active_items,
    }
    return render(request, 'index.html', context)


class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.filter(parent=None, is_active=True)
    serializer_class = MenuItemSerializer

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['GET'])

def customers(request):
  customers = [
    {
      "id": 1,
      "name": "Alex Smith",
      "email": "alex.smith@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=1"
      },
      "status": "subscribed",
      "location": "New York, USA"
    },
    {
      "id": 2,
      "name": "Jordan Brown",
      "email": "jordan.brown@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=2"
      },
      "status": "unsubscribed",
      "location": "London, UK"
    },
    {
      "id": 3,
      "name": "Taylor Green",
      "email": "taylor.green@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=3"
      },
      "status": "bounced",
      "location": "Paris, France"
    },
    {
      "id": 4,
      "name": "Morgan White",
      "email": "morgan.white@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=4"
      },
      "status": "subscribed",
      "location": "Berlin, Germany"
    },
    {
      "id": 5,
      "name": "Casey Gray",
      "email": "casey.gray@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=5"
      },
      "status": "subscribed",
      "location": "Tokyo, Japan"
    },
    {
      "id": 6,
      "name": "Jamie Johnson",
      "email": "jamie.johnson@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=6"
      },
      "status": "subscribed",
      "location": "Sydney, Australia"
    },
    {
      "id": 7,
      "name": "Riley Davis",
      "email": "riley.davis@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=7"
      },
      "status": "subscribed",
      "location": "New York, USA"
    },
    {
      "id": 8,
      "name": "Kelly Wilson",
      "email": "kelly.wilson@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=8"
      },
      "status": "subscribed",
      "location": "London, UK"
    },
    {
      "id": 9,
      "name": "Drew Moore",
      "email": "drew.moore@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=9"
      },
      "status": "bounced",
      "location": "Paris, France"
    },
    {
      "id": 10,
      "name": "Jordan Taylor",
      "email": "jordan.taylor@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=10"
      },
      "status": "subscribed",
      "location": "Berlin, Germany"
    },
    {
      "id": 11,
      "name": "Morgan Anderson",
      "email": "morgan.anderson@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=11"
      },
      "status": "subscribed",
      "location": "Tokyo, Japan"
    },
    {
      "id": 12,
      "name": "Casey Thomas",
      "email": "casey.thomas@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=12"
      },
      "status": "unsubscribed",
      "location": "Sydney, Australia"
    },
    {
      "id": 13,
      "name": "Jamie Jackson",
      "email": "jamie.jackson@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=13"
      },
      "status": "unsubscribed",
      "location": "New York, USA"
    },
    {
      "id": 14,
      "name": "Riley White",
      "email": "riley.white@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=14"
      },
      "status": "unsubscribed",
      "location": "London, UK"
    },
    {
      "id": 15,
      "name": "Kelly Harris",
      "email": "kelly.harris@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=15"
      },
      "status": "subscribed",
      "location": "Paris, France"
    },
    {
      "id": 16,
      "name": "Drew Martin",
      "email": "drew.martin@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=16"
      },
      "status": "subscribed",
      "location": "Berlin, Germany"
    },
    {
      "id": 17,
      "name": "Alex Thompson",
      "email": "alex.thompson@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=17"
      },
      "status": "unsubscribed",
      "location": "Tokyo, Japan"
    },
    {
      "id": 18,
      "name": "Jordan Garcia",
      "email": "jordan.garcia@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=18"
      },
      "status": "subscribed",
      "location": "Sydney, Australia"
    },
    {
      "id": 19,
      "name": "Taylor Rodriguez",
      "email": "taylor.rodriguez@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=19"
      },
      "status": "bounced",
      "location": "New York, USA"
    },
    {
      "id": 20,
      "name": "Morgan Lopez",
      "email": "morgan.lopez@example.com",
      "avatar": {
        "src": "https://i.pravatar.cc/128?u=20"
      },
      "status": "subscribed",
      "location": "London, UK"
    }
  ]

  return JsonResponse(customers, safe=False)

def menu_items(request):
  app_list = []

  for app_config in apps.get_app_configs():
    app_name = app_config.name
    app_label = app_config.label

    # Skip Django built-ins if desired
    if app_name not in LOCAL_APPS:
      continue

    # Get app-level configuration
    app_item = {
      'label': app_config.verbose_name or app_config.label.title(),
      'to': getattr(app_config, 'route', f'/{app_label}'),
      'icon': getattr(app_config, 'icon', 'i-lucide-file-question-mark'),
      'defaultOpen': getattr(app_config, 'default_open', False),
      'type': getattr(app_config, 'nav_type', 'trigger'),
    }

    app_urls = importlib.import_module(f'{app_label}.urls')
    app_urls=app_urls.urlpatterns

    app_item['children'] = []

    for url in app_urls:
      app_item['children'].append({
        'label': url.name,
        'to': f'/{app_label}/{url.name}',
      })

    app_list.append(app_item)

  return JsonResponse(app_list, safe=False)
