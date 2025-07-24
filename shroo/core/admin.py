from django.contrib import admin
from .models import UserPreferences

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_mode', 'menu_mode', 'language', 'updated_at')
    list_filter = ('theme_mode', 'menu_mode', 'language')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')