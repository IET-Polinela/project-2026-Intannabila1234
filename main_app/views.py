from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Report

# Fungsi pembantu untuk mengecek apakah user adalah admin
def is_admin(user):
    return user.is_authenticated and user.is_admin

# Custom decorator untuk admin dengan pesan error
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login terlebih dahulu.")
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, "Akses Ditolak! Hanya Admin yang dapat mengakses fitur ini.")
            return redirect('main_app:reports_list')
        return view_func(request, *args, **kwargs)
    return wrapper

# 1. Menampilkan Daftar Laporan (Dapat dilihat semua orang)
def reports_list(request):
    reports = Report.objects.all().order_by('-id')
    return render(request, 'reports_list.html', {'reports': reports})

# 2. Menambah Laporan Baru (Hanya Admin)
@admin_required
def create_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        Report.objects.create(title=title, location=location, status='REPORTED')
        messages.success(request, "Laporan berhasil dibuat!") # Feedback Lab 6
        return redirect('main_app:reports_list')
    return render(request, 'create_report.html')

# 3. Verifikasi Laporan (Hanya Admin)
@admin_required
def verify_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'VERIFIED'
    report.save()
    messages.info(request, f"Laporan {report.title} telah diverifikasi.")
    return redirect('main_app:reports_list')

# 4. Mulai Pengerjaan (Hanya Admin)
@admin_required
def progress_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'IN_PROGRESS'
    report.save()
    messages.warning(request, "Status laporan: Dalam Pengerjaan.")
    return redirect('main_app:reports_list')

# 5. Tandai Selesai (Hanya Admin)
@admin_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, "Laporan selesai ditangani!")
    return redirect('main_app:reports_list')

# 6. Update/Edit Laporan (Hanya Admin)
@admin_required
def update_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        report.title = request.POST.get('title')
        report.location = request.POST.get('location')
        report.save()
        messages.success(request, "Data laporan berhasil diubah.")
        return redirect('main_app:reports_list')
    return render(request, 'update_report.html', {'report': report})

# 7. Hapus Laporan (Hanya Admin)
@admin_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    messages.error(request, "Laporan telah dihapus secara permanen.")
    return redirect('main_app:reports_list')