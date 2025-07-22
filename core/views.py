from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
import json
from django.http import HttpResponseNotAllowed


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