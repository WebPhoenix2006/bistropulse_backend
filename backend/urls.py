from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # For health check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/customers/', include('customers.urls')),

    # Health check endpoint for Render
    path('api/health/', TemplateView.as_view(template_name='health_check.html'), name='health-check'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

