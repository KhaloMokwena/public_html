from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import Http404, JsonResponse, FileResponse
from django.utils.text import slugify
import os
from django.urls import reverse
from urllib.parse import urlencode
from django.views.decorators.http import require_POST

from .models import Record, Service, JobPosting, Faq, Division, ContactMessage, ContentBlock, JobApplication
from .forms import (
    RecordForm, PageContentForm, ServiceForm, JobPostingForm, FaqForm, DivisionForm, ContactForm,
    ApplicationForm, media_queryset,
)
from .content import PAGES, CAREER_FILTERS, department_group
from .search import run_search, MIN_LENGTH
from .notifications import notify_application, notify_contact, page_value


# --- PUBLIC FRONTEND VIEWS ---

def public_home_view(request):
    """Full-screen hero, a real sector strip and a few honest numbers about the business"""
    services = Service.objects.all()
    sectors = list(dict.fromkeys(s.category for s in services))
    stats = [
        {'value': str(len(sectors)), 'label': 'Industries served'},
        {'value': str(services.count()), 'label': 'Services offered'},
        {'value': str(Division.objects.count()), 'label': 'Specialist divisions'},
        {'value': 'Centurion, SA', 'label': 'Based in'},
    ]
    return render(request, 'pages/home.html', {'sectors': sectors, 'stats': stats})

def about_view(request):
    """Capabilities profile: divisions, FAQs and the media gallery"""
    return render(request, 'pages/about.html', {
        'divisions': Division.objects.all(),
        'faqs': Faq.objects.all().order_by('order', 'id'),
        'gallery': media_queryset().filter(show_in_gallery=True),
    })

def services_view(request):
    """Filterable service catalogue"""
    services = list(Service.objects.all().order_by('order', 'id'))
    sectors = list(dict.fromkeys(s.category for s in services))   # first-appearance order
    return render(request, 'pages/services.html', {'services': services, 'sectors': sectors})

def careers_view(request):
    """Filterable job listings"""
    jobs = list(JobPosting.objects.filter(is_active=True).order_by('-created_at', '-id'))
    present = set()
    for job in jobs:
        job.group = department_group(job.department)
        present.add(job.group)
    groups = [name for name, _ in CAREER_FILTERS if name in present]
    if 'Other' in present:
        groups.append('Other')
    return render(request, 'pages/careers.html', {'jobs': jobs, 'groups': groups})

def contact_view(request):
    """Contact page: details on the left, enquiry form on the right (saved to the inbox in /manage/)"""
    if request.method == 'POST':
        if request.POST.get('website'):
            # Hidden honeypot field: humans leave it empty, bots fill it. Pretend it worked.
            return redirect('contact_thanks')
        form = ContactForm(request.POST)
        if form.is_valid():
            notify_contact(form.save())
            return redirect('contact_thanks')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def contact_thanks_view(request):
    """Shown after a contact enquiry is sent, with a way back to the site."""
    return render(request, 'pages/thanks.html', {
        'heading': page_value('contact', 'success_heading'), 'text': page_value('contact', 'success_text'),
        'primary_url': reverse('home'), 'primary_label': 'Back to Home',
        'secondary_url': reverse('contact'), 'secondary_label': 'Send another message',
    })

def apply_view(request, pk):
    """Apply for one job: details + CV. Saved to /manage/applications/ and emailed to HR."""
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    if request.method == 'POST':
        if request.POST.get('website'):
            # Hidden honeypot field: humans leave it empty, bots fill it. Pretend it worked.
            return redirect('apply_thanks', pk=job.pk)
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.role = job.title
            application.save()
            notify_application(application)   # never raises; the application is already saved
            return redirect('apply_thanks', pk=job.pk)
    else:
        form = ApplicationForm()
    return render(request, 'pages/apply.html', {'job': job, 'form': form})

def apply_thanks_view(request, pk):
    """Shown after a job application is sent. The role may since have closed, so this doesn't require is_active."""
    job = get_object_or_404(JobPosting, pk=pk)
    return render(request, 'pages/thanks.html', {
        'heading': page_value('careers', 'apply_success_heading'), 'text': page_value('careers', 'apply_success_text'),
        'primary_url': reverse('careers'), 'primary_label': 'Back to Careers',
        'secondary_url': reverse('home'), 'secondary_label': 'Back to Home',
    })

def record_detail_view(request, pk):
    """Public detail view for single content items"""
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'dashboard/record_detail.html', {'record': record})

def search_view(request):
    """
    Search every page. Exactly one match: go straight to it. Otherwise show the results.
    """
    query = request.GET.get('q', '').strip()
    results = run_search(query)
    if len(results) == 1:
        return redirect(results[0]['url'])
    return render(request, 'pages/search.html', {
        'q': query,
        'results': results,
        'too_short': bool(query) and len(query) < MIN_LENGTH,
    })

def search_suggest_view(request):
    """JSON for the search box dropdown (top matches only)."""
    query = request.GET.get('q', '').strip()
    results = run_search(query)
    return JsonResponse({
        'total': len(results),
        'all_url': reverse('search') + '?' + urlencode({'q': query}),
        'results': [
            {'title': r['title'], 'kind': r['kind'], 'page': r['page'], 'url': r['url']}
            for r in results[:6]
        ],
    })


# --- SECURE MANAGEMENT ---

# Everything under /manage/ edits the public site, so it needs a staff login
# (same login as /admin/).
staff_required = user_passes_test(lambda u: u.is_active and u.is_staff)

# Editable lists: URL kind -> model, form, labels and the public page they appear on.
COLLECTIONS = {
    'services': {'model': Service, 'form': ServiceForm, 'label': 'Service', 'label_plural': 'Services', 'page': 'services'},
    'jobs': {'model': JobPosting, 'form': JobPostingForm, 'label': 'Job posting', 'label_plural': 'Job postings', 'page': 'careers'},
    'faqs': {'model': Faq, 'form': FaqForm, 'label': 'FAQ', 'label_plural': 'FAQs', 'page': 'about'},
    'divisions': {'model': Division, 'form': DivisionForm, 'label': 'Division', 'label_plural': 'Divisions', 'page': 'about'},
}


def _collection_or_404(kind):
    collection = COLLECTIONS.get(kind)
    if collection is None:
        raise Http404("Unknown content type")
    return collection


@staff_required
def manage_home_view(request):
    """Overview: one card per public page."""
    edited = {
        row['page']: row['n']
        for row in ContentBlock.objects.values('page').annotate(n=Count('id'))
    }
    pages = []
    for slug, cfg in PAGES.items():
        pages.append({
            'slug': slug,
            'label': cfg['label'],
            'url_name': cfg['url_name'],
            'text_total': len(cfg['blocks']),
            'text_edited': edited.get(slug, 0),
            'collections': [
                {
                    'label_plural': COLLECTIONS[k]['label_plural'],
                    'count': COLLECTIONS[k]['model'].objects.count(),
                }
                for k in cfg['collections']
            ],
        })
    return render(request, 'manage/hub.html', {
        'active': 'overview',
        'pages': pages,
        'record_count': Record.objects.count(),
        'unhandled': ContactMessage.objects.filter(handled=False).count(),
        'unhandled_applications': JobApplication.objects.filter(handled=False).count(),
    })


@staff_required
def page_edit_view(request, slug):
    """Edit one page's text and media slots, plus any list (services / jobs / FAQs / divisions) shown on it."""
    cfg = PAGES.get(slug)
    if cfg is None:
        raise Http404("Unknown page")

    if request.method == 'POST':
        form = PageContentForm(slug, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{cfg['label']} page saved.")
            return redirect('page_edit', slug=slug)
    else:
        form = PageContentForm(slug)

    collections = []
    for kind in cfg['collections']:
        c = COLLECTIONS[kind]
        collections.append({
            'kind': kind,
            'label': c['label'],
            'label_plural': c['label_plural'],
            'rows': c['model'].objects.all(),
        })

    return render(request, 'manage/page_edit.html', {
        'active': slug,
        'slug': slug,
        'page': cfg,
        'form': form,
        'collections': collections,
        'edited_count': ContentBlock.objects.filter(page=slug).count(),
        'has_media_slots': any(b.get('type') == 'media' for b in cfg['blocks']),
    })


@staff_required
@require_POST
def page_reset_view(request, slug):
    """Throw away every edit on a page and go back to the defaults."""
    cfg = PAGES.get(slug)
    if cfg is None:
        raise Http404("Unknown page")
    ContentBlock.objects.filter(page=slug).delete()
    messages.success(request, f"{cfg['label']} page restored to the defaults.")
    return redirect('page_edit', slug=slug)


@staff_required
def item_form_view(request, kind, pk=None):
    """Add (no pk) or edit (pk) a service / job posting / FAQ / division."""
    collection = _collection_or_404(kind)
    instance = get_object_or_404(collection['model'], pk=pk) if pk else None

    if request.method == 'POST':
        form = collection['form'](request.POST, instance=instance)
        if form.is_valid():
            form.save()
            verb = 'updated' if instance else 'added'
            messages.success(request, f"{collection['label']} {verb}.")
            return redirect('page_edit', slug=collection['page'])
    else:
        form = collection['form'](instance=instance)

    return render(request, 'manage/item_form.html', {
        'active': collection['page'],
        'form': form,
        'collection': collection,
        'page': PAGES[collection['page']],
        'instance': instance,
    })


@staff_required
def item_delete_view(request, kind, pk):
    collection = _collection_or_404(kind)
    instance = get_object_or_404(collection['model'], pk=pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{collection['label']} deleted.")
        return redirect('page_edit', slug=collection['page'])
    return render(request, 'manage/item_confirm_delete.html', {
        'active': collection['page'],
        'collection': collection,
        'page': PAGES[collection['page']],
        'instance': instance,
    })


# --- CONTACT INBOX ---

@staff_required
def inbox_view(request):
    return render(request, 'manage/inbox.html', {
        'active': 'inbox',
        'enquiries': ContactMessage.objects.all(),
    })


@staff_required
@require_POST
def inbox_toggle_view(request, pk):
    enquiry = get_object_or_404(ContactMessage, pk=pk)
    enquiry.handled = not enquiry.handled
    enquiry.save(update_fields=['handled'])
    return redirect('inbox')


@staff_required
@require_POST
def inbox_delete_view(request, pk):
    get_object_or_404(ContactMessage, pk=pk).delete()
    messages.success(request, "Enquiry deleted.")
    return redirect('inbox')


# --- JOB APPLICATIONS INBOX ---

@staff_required
def applications_view(request):
    return render(request, 'manage/applications.html', {
        'active': 'applications',
        'applications': JobApplication.objects.all(),
    })


@staff_required
@require_POST
def application_toggle_view(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    application.handled = not application.handled
    application.save(update_fields=['handled'])
    return redirect('applications')


@staff_required
@require_POST
def application_delete_view(request, pk):
    get_object_or_404(JobApplication, pk=pk).delete()   # also removes the stored CV file
    messages.success(request, "Application and its CV deleted.")
    return redirect('applications')


@staff_required
def application_cv_view(request, pk):
    """Staff-only CV download. CVs are private files: they have no public URL."""
    application = get_object_or_404(JobApplication, pk=pk)
    if not application.cv:
        raise Http404("No CV on file")
    extension = os.path.splitext(application.cv.name)[1].lower()
    filename = f"{slugify(application.name) or 'candidate'}-{slugify(application.role) or 'application'}{extension}"
    return FileResponse(application.cv.open('rb'), as_attachment=True, filename=filename)


# --- MEDIA LIBRARY (Records) ---

@staff_required
def dashboard_list_view(request):
    """Media library"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_list.html', {'records': records, 'active': 'records'})

@staff_required
def record_create_view(request):
    """Add media"""
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Added to the Media library.")
            return redirect('record_list')
    else:
        form = RecordForm()
    return render(request, 'dashboard/record_form.html', {'form': form, 'action': 'Add', 'active': 'records'})

@staff_required
def record_edit_view(request, pk):
    """Edit media"""
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Media updated.")
            return redirect('record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'dashboard/record_form.html', {'form': form, 'action': 'Edit', 'record': record, 'active': 'records'})

@staff_required
def record_delete_view(request, pk):
    """Delete media"""
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Media deleted.")
        return redirect('record_list')
    return render(request, 'dashboard/record_confirm_delete.html', {'record': record, 'active': 'records'})
