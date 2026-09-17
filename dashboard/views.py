from django.shortcuts import render, redirect
from .models import Record
from django.contrib.auth.decorators import login_required
from .forms import RecordForm

def dashboard_view(request):
    """Internal management view with the form and table"""
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/index.html', {'form': form, 'records': records})

def public_home_view(request):
    """Public-facing frontend view for end users"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/public_home.html', {'records': records})

@login_required  # <--- Restricts this view to logged-in users only
def dashboard_view(request):
    if request.method == 'POST':
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = RecordForm()
    
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/index.html', {'form': form, 'records': records})

def public_home_view(request):
    """Public-facing frontend view remains open to everyone"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/public_home.html', {'records': records})