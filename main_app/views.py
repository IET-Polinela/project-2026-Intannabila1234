from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Report

# 1. LIST DATA & EMPTY STATE
def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'reports_list.html', {'reports': reports})

# 2. CREATE DENGAN FEEDBACK
def create_report(request):
    if request.method == "POST":
        title = request.POST.get('title')
        location = request.POST.get('location')
        
        if title and location:
            Report.objects.create(title=title, location=location, status="REPORTED")
            messages.success(request, "Laporan berhasil ditambahkan!")
            return redirect('reports_list')
    return render(request, 'form.html')

# 3. UPDATE
def update_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        report.title = request.POST.get('title')
        report.location = request.POST.get('location')
        report.save()
        messages.success(request, "Laporan berhasil diperbarui!")
        return redirect('reports_list')
    return render(request, 'form.html', {'report': report})

# 4. DELETE
def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.delete()
    messages.success(request, "Laporan telah dihapus!")
    return redirect('reports_list')

# 5. WORKFLOW LOGIC (Poin 5)
def verify_report(request, id):
    report = get_object_or_404(Report, id=id)
    if report.status == "REPORTED":
        report.status = "VERIFIED"
        report.save()
        messages.success(request, "Status berhasil diverifikasi!")
    return redirect('reports_list')

def progress_report(request, id):
    report = get_object_or_404(Report, id=id)
    if report.status == "VERIFIED":
        report.status = "IN_PROGRESS"
        report.save()
        messages.success(request, "Laporan sekarang sedang diproses.")
    return redirect('reports_list')

def resolve_report(request, id):
    report = get_object_or_404(Report, id=id)
    if report.status == "IN_PROGRESS":
        report.status = "RESOLVED"
        report.save()
        messages.success(request, "Laporan telah diselesaikan!")
    return redirect('reports_list')