from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API endpoints
router = DefaultRouter()
# Future ViewSets will be registered here
# Example: router.register(r'items', ItemViewSet)

app_name = 'core'

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Health check
    path('health/', views.health_check, name='health_check'),

    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),

    # User endpoints
    path('users/me/', views.current_user, name='current_user'),
    path('users/me/update/', views.update_profile, name='update_profile'),
]