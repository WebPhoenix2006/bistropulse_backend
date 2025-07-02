from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView  # For health check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/restaurants/', include('restaurants.urls')), 
    path('api/customers/', include('customers.urls')),
    
    # Health check endpoint (required for Render.com)
    path('api/health/', TemplateView.as_view(template_name='health_check.html'), name='health-check'),
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, ensure MEDIA_URL and STATIC_URL are properly configured
    # with your CDN or storage backend (S3, etc.)
    pass