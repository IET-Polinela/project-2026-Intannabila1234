from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count, Q
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

    # Data untuk Dashboard
    total_reports = Report.objects.count()
    total_reported = Report.objects.filter(status='REPORTED').count()
    total_verified = Report.objects.filter(status='VERIFIED').count()
    total_in_progress = Report.objects.filter(status='IN_PROGRESS').count()
    total_resolved = Report.objects.filter(status='RESOLVED').count()

    # Statistik kategori
    categories = Report.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')

    context = {
        'reports': reports,
        # Dashboard data
        'total_reports': total_reports,
        'total_reported': total_reported,
        'total_verified': total_verified,
        'total_in_progress': total_in_progress,
        'total_resolved': total_resolved,
        'categories': list(categories),
    }

    return render(request, 'reports_list.html', context)

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

# 8. Search Reports (JSON) - LIVE SEARCH API
def search_reports(request):
    """
    API untuk Live Search Laporan
    - Menerima parameter query (?q=)
    - Filter berdasarkan title (icontains)
    - Return JsonResponse dengan list data laporan
    - Jika query kosong, return 20 laporan terbaru
    """
    query = request.GET.get('q', '').strip()

    if query:
        # Cari berdasarkan title saja (sesuai permintaan)
        reports = Report.objects.filter(title__icontains=query)
    else:
        # Jika tidak ada query, tampilkan semua laporan terbaru
        reports = Report.objects.all()

    # Limit 20 hasil, urutkan berdasarkan ID terbaru
    reports = reports.order_by('-id')[:20]

    # Format data untuk JSON response
    data = []
    for report in reports:
        data.append({
            'id': report.id,
            'title': report.title,
            'location': report.location,
            'category': report.category,
            'status': report.status,
        })

    return JsonResponse(data, safe=False)


# 9. Report Detail (JSON) - MODAL DETAIL API
def report_detail(request, report_id):
    """
    API untuk Detail Laporan (untuk Modal)
    - Menerima report_id dari URL
    - Return JsonResponse dengan detail lengkap laporan
    - Include semua field: id, title, location, category, status, description
    """
    try:
        report = Report.objects.get(id=report_id)
        data = {
            'id': report.id,
            'title': report.title,
            'location': report.location,
            'category': report.category,
            'status': report.status,
            'description': report.description,
        }
        return JsonResponse(data)
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Laporan tidak ditemukan'}, status=404)


# ============================================================
# DASHBOARD - CLASS-BASED VIEW & API ENDPOINTS (Lab Session 7)
# ============================================================

class DashboardView(TemplateView):
    """
    Dashboard menggunakan Class-Based View (TemplateView).
    Menampilkan halaman dashboard dengan chart dan statistik.
    """
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        """
        Menyediakan context data untuk template.
        Menghitung total laporan berdasarkan status.
        """
        context = super().get_context_data(**kwargs)
        
        # Hitung total laporan per status
        total_reported = Report.objects.filter(status='REPORTED').count()
        total_verified = Report.objects.filter(status='VERIFIED').count()
        total_in_progress = Report.objects.filter(status='IN_PROGRESS').count()
        total_resolved = Report.objects.filter(status='RESOLVED').count()
        
        # Hitung total laporan
        context['total_reports'] = Report.objects.count()
        context['total_reported'] = total_reported
        context['total_verified'] = total_verified
        context['total_in_progress'] = total_in_progress
        context['total_resolved'] = total_resolved
        
        return context


def api_status_statistics(request):
    """
    API ENDPOINT: Statistik Status Laporan
    
    Mengembalikan JSON berisi count laporan per status.
    Format: {
        'REPORTED': 5,
        'VERIFIED': 3,
        'IN_PROGRESS': 2,
        'RESOLVED': 4
    }
    """
    statistics = {
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    }
    
    return JsonResponse(statistics)


def api_category_statistics(request):
    """
    API ENDPOINT: Statistik Kategori Laporan
    
    Mengembalikan JSON berisi count laporan per kategori.
    Format: {
        'Infrastructure': 5,
        'Pothole': 3,
        'etc': 2
    }
    """
    # Query untuk menghitung laporan per kategori
    categories = Report.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Convert ke dictionary
    statistics = {item['category']: item['count'] for item in categories}
    
    return JsonResponse(statistics)


def api_latest_reported(request):
    """
    API ENDPOINT: 5 Laporan Terbaru Status REPORTED
    
    Mengembalikan JSON berisi 5 laporan terbaru dengan status REPORTED.
    Format: [
        {
            'id': 1,
            'title': 'Jalan Rusak di Jl. Merdeka',
            'location': 'Jl. Merdeka No.10',
            'category': 'Pothole',
            'status': 'REPORTED'
        },
        ...
    ]
    """
    reports = Report.objects.filter(
        status='REPORTED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)


def api_latest_resolved(request):
    """
    API ENDPOINT: 5 Laporan Terbaru Status RESOLVED
    
    Mengembalikan JSON berisi 5 laporan terbaru dengan status RESOLVED.
    Format: [
        {
            'id': 1,
            'title': 'Jalan Rusak di Jl. Merdeka',
            'location': 'Jl. Merdeka No.10',
            'category': 'Pothole',
            'status': 'RESOLVED'
        },
        ...
    ]
    """
    reports = Report.objects.filter(
        status='RESOLVED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)


def api_search_reports(request):
    """
    API ENDPOINT: Live Search Laporan

    Mencari laporan berdasarkan query parameter 'q'.
    Mencari di field title, location, dan category.

    Jika query kosong, kembalikan 20 laporan terbaru sebagai fallback.
    Format: [
        {
            'id': 1,
            'title': 'Jalan Rusak',
            'location': 'Jl. Merdeka',
            'status': 'REPORTED'
        },
        ...
    ]
    """
    query = request.GET.get('q', '').strip()

    if not query:
        reports = Report.objects.order_by('-id').values(
            'id', 'title', 'location', 'category', 'status'
        )[:20]
    else:
        reports = Report.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        ).values('id', 'title', 'location', 'category', 'status').order_by('-id')[:20]

    return JsonResponse(list(reports), safe=False)


def api_report_detail(request, report_id):
    """
    API ENDPOINT: Detail Laporan
    
    Mengembalikan detail lengkap satu laporan dalam format JSON.
    Format: {
        'id': 1,
        'title': 'Jalan Rusak di Jl. Merdeka',
        'location': 'Jl. Merdeka No.10',
        'category': 'Pothole',
        'description': 'Jalan berlubang besar...',
        'status': 'REPORTED'
    }
    """
    try:
        report = Report.objects.get(id=report_id)
        data = {
            'id': report.id,
            'title': report.title,
            'location': report.location,
            'category': report.category,
            'description': report.description,
            'status': report.status,
        }
        return JsonResponse(data)
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Laporan tidak ditemukan'}, status=404)