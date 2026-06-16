"""
Dashboard Views - Lab Session 7
Menggunakan Class-Based View (TemplateView) dan JsonResponse
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count, Q
from main_app.models import Report


class DashboardView(TemplateView):
    """
    Class-Based View untuk Dashboard menggunakan TemplateView.
    
    Fitur:
    - Menampilkan template dashboard/index.html
    - Mengirim context data statistik ke template
    - Sesuai requirement Lab Session 7
    
    URL: /dashboard/
    """
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        """
        Override method untuk menambahkan context data.
        Context ini akan dikirim ke template.
        """
        context = super().get_context_data(**kwargs)
        
        # ========================================
        # Hitung Statistik Status Laporan
        # ========================================
        total_reports = Report.objects.count()
        reported_count = Report.objects.filter(status='REPORTED').count()
        verified_count = Report.objects.filter(status='VERIFIED').count()
        in_progress_count = Report.objects.filter(status='IN_PROGRESS').count()
        resolved_count = Report.objects.filter(status='RESOLVED').count()
        
        # ========================================
        # Hitung Statistik Kategori Laporan
        # ========================================
        category_stats = (
            Report.objects
            .values('category')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Masukkan ke context
        context['total_reports'] = total_reports
        context['reported_count'] = reported_count
        context['verified_count'] = verified_count
        context['in_progress_count'] = in_progress_count
        context['resolved_count'] = resolved_count
        context['category_stats'] = list(category_stats)
        
        return context


def dashboard_data(request):
    """
    API Endpoint untuk mendapatkan data statistik dalam format JSON.
    
    Digunakan oleh Chart.js untuk fetch data dan render charts.
    Response format:
    {
        'status': {
            'REPORTED': 5,
            'VERIFIED': 3,
            'IN_PROGRESS': 2,
            'RESOLVED': 4
        },
        'categories': {
            'Pothole': 5,
            'Infrastructure': 3,
            'Other': 2
        },
        'total': 14
    }
    
    Endpoint: /dashboard/api/data/
    Method: GET
    """
    
    # ========================================
    # Statistik Status Laporan
    # ========================================
    status_stats = {
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    }
    
    # ========================================
    # Statistik Kategori Laporan (ORM Aggregation)
    # ========================================
    category_data = (
        Report.objects
        .values('category')  # GROUP BY kategori
        .annotate(count=Count('id'))  # SELECT COUNT(id)
        .order_by('-count')  # ORDER BY count DESC
    )
    
    # Convert queryset ke dictionary
    category_stats = {item['category']: item['count'] for item in category_data}
    
    # ========================================
    # Total Laporan
    # ========================================
    total = Report.objects.count()
    
    # ========================================
    # Buat Response JSON
    # ========================================
    data = {
        'status': status_stats,
        'categories': category_stats,
        'total': total,
    }
    
    return JsonResponse(data, safe=False)


def latest_reported(request):
    """
    API Endpoint untuk mendapatkan 5 laporan terbaru dengan status REPORTED.
    
    Response format:
    [
        {
            'id': 1,
            'title': 'Jalan Rusak',
            'location': 'Jl. Merdeka',
            'category': 'Pothole',
            'status': 'REPORTED'
        },
        ...
    ]
    
    Endpoint: /dashboard/api/latest-reported/
    Method: GET
    """
    reports = (
        Report.objects
        .filter(status='REPORTED')
        .order_by('-id')
        .values('id', 'title', 'location', 'category', 'status')
        [:5]
    )
    
    return JsonResponse(list(reports), safe=False)


def latest_resolved(request):
    """
    API Endpoint untuk mendapatkan 5 laporan terbaru dengan status RESOLVED.
    
    Response format: sama seperti latest_reported
    
    Endpoint: /dashboard/api/latest-resolved/
    Method: GET
    """
    reports = (
        Report.objects
        .filter(status='RESOLVED')
        .order_by('-id')
        .values('id', 'title', 'location', 'category', 'status')
        [:5]
    )
    
    return JsonResponse(list(reports), safe=False)
