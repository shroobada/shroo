from rest_framework import serializers
from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'label', 'icon', 'to', 'url', 'items']

    def get_items(self, obj):
        if obj.items.filter(is_active=True).exists():
            return MenuItemSerializer(obj.items.filter(is_active=True), many=True).data
        return None