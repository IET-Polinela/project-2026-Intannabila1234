# LAB SESSION 7: Kode Lengkap Untuk Referensi

## File: main_app/views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count, Q
from .models import Report

# ============================================================
# EXISTING FUNCTIONS (sudah ada sebelumnya)
# ============================================================

def is_admin(user):
    return user.is_authenticated and user.is_admin

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

def reports_list(request):
    reports = Report.objects.all().order_by('-id')
    return render(request, 'reports_list.html', {'reports': reports})

@admin_required
def create_report(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        Report.objects.create(title=title, location=location, status='REPORTED')
        messages.success(request, "Laporan berhasil dibuat!")
        return redirect('main_app:reports_list')
    return render(request, 'create_report.html')

@admin_required
def verify_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'VERIFIED'
    report.save()
    messages.info(request, f"Laporan {report.title} telah diverifikasi.")
    return redirect('main_app:reports_list')

@admin_required
def progress_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'IN_PROGRESS'
    report.save()
    messages.warning(request, "Status laporan: Dalam Pengerjaan.")
    return redirect('main_app:reports_list')

@admin_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, "Laporan selesai ditangani!")
    return redirect('main_app:reports_list')

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

@admin_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    messages.error(request, "Laporan telah dihapus secara permanen.")
    return redirect('main_app:reports_list')

def search_reports(request):
    q = request.GET.get('q', '')
    reports = Report.objects.filter(title__icontains=q) | Report.objects.filter(location__icontains=q)
    data = [{'id': r.id, 'title': r.title, 'status': r.status} for r in reports]
    return JsonResponse(data, safe=False)

def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    data = {'title': report.title, 'status': report.status}
    return JsonResponse(data)


# ============================================================
# NEW: DASHBOARD & API ENDPOINTS (Lab Session 7)
# ============================================================

class DashboardView(TemplateView):
    """Dashboard menggunakan Class-Based View (TemplateView)"""
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_reported = Report.objects.filter(status='REPORTED').count()
        total_verified = Report.objects.filter(status='VERIFIED').count()
        total_in_progress = Report.objects.filter(status='IN_PROGRESS').count()
        total_resolved = Report.objects.filter(status='RESOLVED').count()
        
        context['total_reports'] = Report.objects.count()
        context['total_reported'] = total_reported
        context['total_verified'] = total_verified
        context['total_in_progress'] = total_in_progress
        context['total_resolved'] = total_resolved
        
        return context


def api_status_statistics(request):
    """API: Statistik Status Laporan"""
    statistics = {
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    }
    return JsonResponse(statistics)


def api_category_statistics(request):
    """API: Statistik Kategori Laporan"""
    categories = Report.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    statistics = {item['category']: item['count'] for item in categories}
    return JsonResponse(statistics)


def api_latest_reported(request):
    """API: 5 Laporan Terbaru Status REPORTED"""
    reports = Report.objects.filter(
        status='REPORTED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)


def api_latest_resolved(request):
    """API: 5 Laporan Terbaru Status RESOLVED"""
    reports = Report.objects.filter(
        status='RESOLVED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)


def api_search_reports(request):
    """API: Live Search Laporan"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(location__icontains=query) |
        Q(category__icontains=query)
    ).values('id', 'title', 'location', 'category', 'status').order_by('-id')[:10]
    
    return JsonResponse(list(reports), safe=False)


def api_report_detail(request, report_id):
    """API: Detail Laporan"""
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
```

---

## File: main_app/urls.py

```python
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Dashboard & Statistik
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # API Endpoints untuk Dashboard
    path('api/status-statistics/', views.api_status_statistics, name='api_status_stats'),
    path('api/category-statistics/', views.api_category_statistics, name='api_category_stats'),
    path('api/latest-reported/', views.api_latest_reported, name='api_latest_reported'),
    path('api/latest-resolved/', views.api_latest_resolved, name='api_latest_resolved'),
    path('api/search/', views.api_search_reports, name='api_search'),
    path('api/detail/<int:report_id>/', views.api_report_detail, name='api_detail'),
    
    # Laporan & CRUD Operations
    path('', views.reports_list, name='reports_list'),
    path('create/', views.create_report, name='create'),
    path('verify/<int:report_id>/', views.verify_report, name='verify'),
    path('progress/<int:report_id>/', views.progress_report, name='progress'),
    path('resolve/<int:report_id>/', views.resolve_report, name='resolve'),
    path('update/<int:report_id>/', views.update_report, name='update'),
    path('delete/<int:report_id>/', views.delete_report, name='delete'),
    path('search/', views.search_reports, name='search'),
    path('detail/<int:report_id>/', views.report_detail, name='detail'),
]
```

---

## File: templates/dashboard.html (HTML dengan Bootstrap & Chart.js)

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Dashboard - Laporan Publik{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
    <!-- Page Title -->
    <div class="row mb-4">
        <div class="col-md-12">
            <h1 class="display-4">📊 Dashboard Laporan Publik</h1>
            <p class="text-muted">Lab Session 7 - Pemrograman Internet 1 | Visualisasi Data & API</p>
            <hr>
        </div>
    </div>

    <!-- Statistik Cards -->
    <div class="row mb-4">
        <div class="col-md-3 mb-3">
            <div class="card bg-primary text-white">
                <div class="card-body">
                    <h5>📝 Total Laporan</h5>
                    <h2>{{ total_reports }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-warning text-white">
                <div class="card-body">
                    <h5>🔔 Reported</h5>
                    <h2>{{ total_reported }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-info text-white">
                <div class="card-body">
                    <h5>⚙️ In Progress</h5>
                    <h2>{{ total_in_progress }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-success text-white">
                <div class="card-body">
                    <h5>✅ Resolved</h5>
                    <h2>{{ total_resolved }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Charts Section -->
    <div class="row mb-4">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5>📈 Statistik Status Laporan</h5>
                </div>
                <div class="card-body">
                    <canvas id="statusChart" height="100"></canvas>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-light">
                    <h5>📊 Statistik Kategori Laporan</h5>
                </div>
                <div class="card-body">
                    <canvas id="categoryChart" height="100"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Live Search Section -->
    <div class="row mb-4">
        <div class="col-md-12">
            <div class="card">
                <div class="card-header bg-light">
                    <h5>🔍 Live Search Laporan</h5>
                </div>
                <div class="card-body">
                    <input type="text" id="searchInput" class="form-control form-control-lg" 
                           placeholder="Cari berdasarkan judul, lokasi, atau kategori...">
                    <div id="searchResults" class="mt-3"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- Latest Reports Section -->
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h5>🔔 5 Laporan Terbaru (REPORTED)</h5>
                </div>
                <div class="card-body p-0">
                    <div id="latestReportedList" class="list-group list-group-flush">
                        <p class="text-muted text-center py-3">Loading...</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 mb-4">
            <div class="card">
                <div class="card-header bg-success text-white">
                    <h5>✅ 5 Laporan Terbaru (RESOLVED)</h5>
                </div>
                <div class="card-body p-0">
                    <div id="latestResolvedList" class="list-group list-group-flush">
                        <p class="text-muted text-center py-3">Loading...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal untuk Detail Laporan -->
<div class="modal fade" id="detailModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="detailModalLabel">Detail Laporan</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div id="modalContent">
                    <p class="text-muted">Loading...</p>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Tutup</button>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
<script src="{% static 'js/dashboard.js' %}"></script>
{% endblock %}
```

---

## File: static/js/dashboard.js (JavaScript Lengkap)

Lihat file `dashboard.js` yang sudah dibuat di folder `static/js/`

---

## Fitur & Penjelasan Singkat

### 1. Class-Based View (TemplateView)
```python
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        # Menghitung statistik dan pass ke template
```
- **Kegunaan**: Render template dengan context data
- **URL**: `/main_app/dashboard/`

### 2. API Endpoints (JsonResponse)
```python
def api_status_statistics(request):
    statistics = {'REPORTED': 5, 'VERIFIED': 3, ...}
    return JsonResponse(statistics)
```
- **Kegunaan**: Return data dalam format JSON untuk Fetch API
- **Tanpa reload**: Frontend fetch data dan render dinamically

### 3. Doughnut Chart (Chart.js)
```javascript
new Chart(ctx, {
    type: 'doughnut',
    data: { labels: [...], datasets: [...] }
})
```
- Menampilkan distribusi status laporan
- Tooltip menunjukkan persentase

### 4. Bar Chart (Chart.js)
```javascript
new Chart(ctx, {
    type: 'bar',
    data: { labels: [...], datasets: [...] }
})
```
- Menampilkan distribusi kategori laporan
- Horizontal bar untuk readability

### 5. Live Search dengan Debouncing
```javascript
const debouncedSearch = debounce(async (q) => {
    const results = await searchReports(q);
    renderSearchResults(results);
}, 300);
```
- Mengurangi API calls saat user mengetik
- Delay 300ms untuk wait hingga user selesai

### 6. Event Delegation untuk Detail Button
```javascript
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('detail-btn')) {
        showDetailModal(e.target.dataset.reportId);
    }
});
```
- Handle click pada dynamis button
- Lebih efisien dari attach listener ke setiap button

### 7. DOMContentLoaded untuk Inisialisasi
```javascript
document.addEventListener('DOMContentLoaded', async () => {
    await renderStatusChart();
    await renderCategoryChart();
    // ... init events
});
```
- Menunggu DOM ready sebelum execute
- Prevent error saat element belum loaded

---

## Testing

```bash
# Access dashboard
http://localhost:8000/main_app/dashboard/

# Test API endpoints
http://localhost:8000/main_app/api/status-statistics/
http://localhost:8000/main_app/api/category-statistics/
http://localhost:8000/main_app/api/latest-reported/
http://localhost:8000/main_app/api/latest-resolved/
http://localhost:8000/main_app/api/search/?q=jalan
http://localhost:8000/main_app/api/detail/1/
```

---

## Kode Mengikuti:
- ✅ PEP8 Style Guide
- ✅ DRY Principle
- ✅ Async/Await Pattern
- ✅ Event Delegation Pattern
- ✅ Template Literals
- ✅ Modern JavaScript (ES6+)

