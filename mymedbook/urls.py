from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),  # Root API endpoint
    path('health/', views.health_check, name='health-check'),  # Health check endpoint
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api/', include('api.urls')),
    
    # Redirect /favicon.ico to your static file if you have one
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

# Add handler for 404 errors
handler404 = 'mymedbook.views.api_root'  # Redirect all unknown paths to API root