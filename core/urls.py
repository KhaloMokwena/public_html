from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import (
    public_home_view, careers_view, about_view, 
    services_view, contact_view, record_detail_view,
    dashboard_list_view, record_create_view,
    record_edit_view, record_delete_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Public Frontend Routes
    path('', public_home_view, name='home'),
    path('about/', about_view, name='about'),
    path('services/', services_view, name='services'),
    path('careers/', careers_view, name='careers'),
    path('contact/', contact_view, name='contact'),
    path('item/<int:pk>/', record_detail_view, name='record_detail'),
    
    # Secure Management & CRUD Routes
    path('manage/', dashboard_list_view, name='dashboard'),
    path('manage/add/', record_create_view, name='record_add'),
    path('manage/<int:pk>/edit/', record_edit_view, name='record_edit'),
    path('manage/<int:pk>/delete/', record_delete_view, name='record_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)