from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API endpoints
router = DefaultRouter()
# Future ViewSets will be registered here

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health_check'),
]