"""
Dashboard views for the SmartCity dashboard.
"""

from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render

from main_app.models import Report


def dashboard(request):
    """
    Render the dashboard and handle report creation submissions.
    """
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        category = (request.POST.get('category') or 'Umum').strip()
        description = (request.POST.get('description') or '').strip()
        location = (request.POST.get('location') or '').strip()
        status = (request.POST.get('status') or 'REPORTED').strip()

        if title and location:
            Report.objects.create(
                title=title,
                category=category or 'Umum',
                description=description,
                location=location,
                reporter=request.user if request.user.is_authenticated else None,
                status=status,
            )
            messages.success(request, 'Laporan berhasil ditambahkan.')
            return redirect('dashboard:dashboard')

        messages.error(request, 'Judul dan lokasi laporan wajib diisi.')
        return redirect('dashboard:dashboard')

    total_reports = Report.objects.count()
    reported_count = Report.objects.filter(status='REPORTED').count()
    verified_count = Report.objects.filter(status='VERIFIED').count()
    in_progress_count = Report.objects.filter(status='IN_PROGRESS').count()
    resolved_count = Report.objects.filter(status='RESOLVED').count()

    category_stats = (
        Report.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    latest_reports = (
        Report.objects
        .filter(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS'])
        .order_by('-created_at')[:5]
    )
    resolved_reports = (
        Report.objects
        .filter(status='RESOLVED')
        .order_by('-updated_at')[:5]
    )
    reports = Report.objects.order_by('-created_at')[:8]

    context = {
        'total_reports': total_reports,
        'reported_count': reported_count,
        'verified_count': verified_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'category_stats': list(category_stats),
        'latest_reports': latest_reports,
        'resolved_reports': resolved_reports,
        'reports': reports,
    }
    return render(request, 'dashboard.html', context)


def dashboard_data(request):
    """
    JSON endpoint for dashboard chart data.
    """
    status_stats = {
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    }

    category_data = (
        Report.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    category_stats = {item['category']: item['count'] for item in category_data}

    data = {
        'status': status_stats,
        'categories': category_stats,
        'total': Report.objects.count(),
    }
    return JsonResponse(data)


def latest_reported(request):
    """
    JSON endpoint for recent reported issues.
    """
    reports = (
        Report.objects
        .filter(status='REPORTED')
        .order_by('-id')
        .values('id', 'title', 'location', 'category', 'status')[:5]
    )
    return JsonResponse(list(reports), safe=False)


def latest_resolved(request):
    """
    JSON endpoint for recent resolved issues.
    """
    reports = (
        Report.objects
        .filter(status='RESOLVED')
        .order_by('-id')
        .values('id', 'title', 'location', 'category', 'status')[:5]
    )
    return JsonResponse(list(reports), safe=False)
