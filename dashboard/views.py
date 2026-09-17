from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Record
from .forms import RecordForm

def public_home_view(request):
    """Public home page showing the grid of all records"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/public_home.html', {'records': records})

def record_detail_view(request, pk):
    """Public detail page for a single item"""
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'dashboard/record_detail.html', {'record': record})

@login_required
def dashboard_list_view(request):
    """Management dashboard: lists all pages/records with management actions"""
    records = Record.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_list.html', {'records': records})

@login_required
def record_create_view(request):
    """Create a new record"""
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
    """Edit an existing record"""
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
    """Delete a record with confirmation"""
    record = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('dashboard')
    return render(request, 'dashboard/record_confirm_delete.html', {'record': record})