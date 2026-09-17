from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Record, Service, JobPosting, Faq
from .forms import RecordForm


# --- PUBLIC FRONTEND VIEWS ---

def public_home_view(request):
    """Full-screen visual anchor home page"""
    return render(request, 'pages/home.html')

def about_view(request):
    """Asymmetric about page with dynamic FAQs"""
    faqs = Faq.objects.all().order_by('order')
    return render(request, 'pages/about.html', {'faqs': faqs})

def services_view(request):
    """Dynamic full-screen service matrices"""
    services = Service.objects.all().order_by('order')
    return render(request, 'pages/services.html', {'services': services})

def careers_view(request):
    """Dynamic terminal job listings"""
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'pages/careers.html', {'jobs': jobs})

def contact_view(request):
    """Minimal glowing line contact form"""
    return render(request, 'pages/contact.html')

def record_detail_view(request, pk):
    """Public detail view for single content items"""
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'dashboard/record_detail.html', {'record': record})


# --- SECURE MANAGEMENT & CRUD VIEWS ---

@login_required
def dashboard_list_view(request):
    """Management list table"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_list.html', {'records': records})

@login_required
def record_create_view(request):
    """Create new record item"""
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    return render(request, 'dashboard/record_form.html', {'form': form, 'action': 'Create'})

@login_required
def record_edit_view(request, pk):
    """Edit existing record item"""
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm(instance=record)
    return render(request, 'dashboard/record_form.html', {'form': form, 'action': 'Edit', 'record': record})

@login_required
def record_delete_view(request, pk):
    """Delete record item"""
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/record_confirm_delete.html', {'record': record})