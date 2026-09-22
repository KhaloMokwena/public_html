from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import (
    public_home_view, careers_view, about_view,
    services_view, contact_view, contact_thanks_view, record_detail_view,
    manage_home_view, page_edit_view, page_reset_view,
    item_form_view, item_delete_view,
    inbox_view, inbox_toggle_view, inbox_delete_view,
    apply_view, apply_thanks_view, applications_view, application_toggle_view, application_delete_view, application_cv_view,
    search_view, search_suggest_view,
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
    path('careers/apply/<int:pk>/', apply_view, name='apply'),
    path('careers/apply/<int:pk>/thank-you/', apply_thanks_view, name='apply_thanks'),
    path('contact/', contact_view, name='contact'),
    path('contact/thank-you/', contact_thanks_view, name='contact_thanks'),
    path('item/<int:pk>/', record_detail_view, name='record_detail'),
    path('search/', search_view, name='search'),
    path('search/suggest/', search_suggest_view, name='search_suggest'),

    # Secure Management: overview + per-page content editor
    path('manage/', manage_home_view, name='dashboard'),
    path('manage/page/<slug:slug>/', page_edit_view, name='page_edit'),
    path('manage/page/<slug:slug>/reset/', page_reset_view, name='page_reset'),

    # Secure Management: services / job postings / FAQs
    path('manage/content/<slug:kind>/add/', item_form_view, name='item_add'),
    path('manage/content/<slug:kind>/<int:pk>/edit/', item_form_view, name='item_edit'),
    path('manage/content/<slug:kind>/<int:pk>/delete/', item_delete_view, name='item_delete'),

    # Secure Management: contact enquiries
    path('manage/inbox/', inbox_view, name='inbox'),
    path('manage/inbox/<int:pk>/toggle/', inbox_toggle_view, name='inbox_toggle'),
    path('manage/inbox/<int:pk>/delete/', inbox_delete_view, name='inbox_delete'),

    # Secure Management: job applications
    path('manage/applications/', applications_view, name='applications'),
    path('manage/applications/<int:pk>/toggle/', application_toggle_view, name='application_toggle'),
    path('manage/applications/<int:pk>/delete/', application_delete_view, name='application_delete'),
    path('manage/applications/<int:pk>/cv/', application_cv_view, name='application_cv'),

    # Secure Management: Media library (Records)
    path('manage/records/', dashboard_list_view, name='record_list'),
    path('manage/add/', record_create_view, name='record_add'),
    path('manage/<int:pk>/edit/', record_edit_view, name='record_edit'),
    path('manage/<int:pk>/delete/', record_delete_view, name='record_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)