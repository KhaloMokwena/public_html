from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import dashboard_view, public_home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', public_home_view, name='home'),          # Public end-user frontend
    path('manage/', dashboard_view, name='dashboard'), # Admin data-entry dashboard
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)