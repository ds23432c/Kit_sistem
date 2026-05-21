from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('equipment/', include('equipment.urls')),
    path('map/', include('map_builder.urls')),
    path('requests/', include('requests_app.urls')),
    path('accounting/', include('accounting.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
