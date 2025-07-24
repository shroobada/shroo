from django.contrib.auth.models import User
from django.db import models


class UserPreferences(models.Model):
    class ColorChoices(models.TextChoices):
        AMBER = 'amber', 'Amber'
        BLUE = 'blue', 'Blue'
        CYAN = 'cyan', 'Cyan'
        EMERALD = 'emerald', 'Emerald'
        FUCHSIA = 'fuchsia', 'Fuchsia'
        GRAY = 'gray', 'Gray'
        GREEN = 'green', 'Green'
        INDIGO = 'indigo', 'Indigo'
        LIME = 'lime', 'Lime'
        ORANGE = 'orange', 'Orange'
        PINK = 'pink', 'Pink'
        PURPLE = 'purple', 'Purple'
        RED = 'red', 'Red'
        ROSE = 'rose', 'Rose'
        SKY = 'sky', 'Sky'
        SLATE = 'slate', 'Slate'
        STONE = 'stone', 'Stone'
        TEAL = 'teal', 'Teal'
        VIOLET = 'violet', 'Violet'
        YELLOW = 'yellow', 'Yellow'
        ZINC = 'zinc', 'Zinc'

    class TintChoices(models.TextChoices):
        TINT_50 = '50', '50'
        TINT_100 = '100', '100'
        TINT_200 = '200', '200'
        TINT_300 = '300', '300'
        TINT_400 = '400', '400'
        TINT_500 = '500', '500'
        TINT_600 = '600', '600'
        TINT_700 = '700', '700'
        TINT_800 = '800', '800'
        TINT_900 = '900', '900'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme_mode = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='dark')
    primevue_theme = models.CharField(max_length=20, choices=[('aura', 'Aura'), ('lara', 'Lara'), ('nora', 'Nora'),
                                                               ('material', 'Material')], default='aura')
    menu_mode = models.CharField(max_length=15,
                                 choices=[('static', 'Static'), ('overlay', 'Overlay')],
                                 default='static')
    primary_color = models.CharField(max_length=10,choices=ColorChoices.choices,default=ColorChoices.EMERALD,)
    primary_tint = models.CharField(max_length=3, choices=TintChoices.choices, default=TintChoices.TINT_500)
    surface_tint = models.CharField(max_length=3, choices=TintChoices.choices, default=TintChoices.TINT_500)
    language = models.CharField(max_length=5, default='en-us')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Preference'
        verbose_name_plural = 'User Preferences'

    def __str__(self):
        return f"{self.user.username} - {self.theme_mode} theme"


class MenuItem(models.Model):
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    to = models.CharField(max_length=200, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'label']

    def __str__(self):
        return self.label
