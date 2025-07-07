from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView  # For health check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapp.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/chat/', include('chat.urls')),


    # Health check endpoint for Render
    path('api/health/', TemplateView.as_view(template_name='health_check.html'), name='health-check'),

    # Media serving in production (Render)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Only serve static files using Django in development
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
