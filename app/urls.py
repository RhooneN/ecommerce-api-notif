from django.urls import path
from .views import NotificationView
from .import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notification-list'),  # Create and retrieve notifications
    path("health/", views.health),
    
     #Swagger
    path(
        "api/schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema",),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[AllowAny]), name='redoc'),
    ]
