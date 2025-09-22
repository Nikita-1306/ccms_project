from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CaseForm
from django.contrib import messages
from datetime import date

def home(request):
    return render(request, 'cases/home.html')

@login_required
def case_create(request):
    today = date.today()
    daily_count = Case.objects.filter(reporter=request.user, created_at__date=today).count()
    if daily_count >= 10:
        messages.error(request, 'Daily limit reached. Try again tomorrow.')
        return redirect('my_cases')
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.reporter = request.user
            c.save()
            messages.success(request, f'Case submitted. Tracking ID: {c.tracking_id}')
            return render(request, 'cases/case_submitted.html', {'case': c})
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form': form})

@login_required
def my_cases(request):
    cases = Case.objects.filter(reporter=request.user).order_by('-created_at')
    return render(request, 'cases/my_cases.html', {'cases': cases})

def case_detail(request, pk):
    c = get_object_or_404(Case, pk=pk)
    if c.reporter != request.user and not request.user.is_staff:
        return render(request, 'cases/case_public_detail.html', {'case': c})
    return render(request, 'cases/case_detail.html', {'case': c})

@login_required
def case_edit(request, pk):
    c = get_object_or_404(Case, pk=pk, reporter=request.user)
    if c.status != 'New':
        messages.error(request, 'Cannot edit case once it is not New.')
        return redirect('my_cases')
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case updated.')
            return redirect('my_cases')
    else:
        form = CaseForm(instance=c)
    return render(request, 'cases/case_form.html', {'form': form, 'edit': True})

@login_required
def case_delete(request, pk):
    c = get_object_or_404(Case, pk=pk, reporter=request.user)
    if c.status != 'New':
        messages.error(request, 'Cannot delete case once it is not New.')
        return redirect('my_cases')
    if request.method == 'POST':
        c.delete()
        messages.success(request, 'Case deleted.')
        return redirect('my_cases')
    return render(request, 'cases/case_confirm_delete.html', {'case': c})

def track_case(request):
    case = None
    if request.method == 'POST':
        tid = request.POST.get('tracking_id','').strip()
        try:
            case = Case.objects.get(tracking_id=tid)
        except Case.DoesNotExist:
            case = None
    return render(request, 'cases/track.html', {'case': case})

from django.http import HttpResponse
from reportlab.pdfgen import canvas

@login_required
def download_report(request, pk):
    case = get_object_or_404(Case, pk=pk, reporter=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="case_{case.id}_report.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Crime Report")
    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Report ID: {case.id}")
    p.drawString(50, 740, f"Tracking ID: {case.tracking_id}")
    p.drawString(50, 720, f"Reported By: {case.reporter.username} ({case.reporter.email})")
    p.drawString(50, 700, f"Crime Type: {case.crime_type}")
    p.drawString(50, 680, f"Description: {case.description}")
    p.drawString(50, 660, f"Date: {case.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, 640, f"Status: {case.status}")

    p.drawString(50, 50, "Signature: ____________________")
    p.showPage()
    p.save()
    return response