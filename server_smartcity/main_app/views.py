from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from .models import Report


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _admin_required(view_func):
    """Dekorator: hanya user dengan is_admin=True yang boleh akses."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Silakan login terlebih dahulu.')
            return redirect('login')
        if not getattr(request.user, 'is_admin', False):
            messages.error(request, 'Akses ditolak. Hanya admin yang dapat mengakses fitur ini.')
            return redirect('main_app:reports_list')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ---------------------------------------------------------------------------
# Template-based views
# ---------------------------------------------------------------------------

def reports_list(request):
    reports = Report.objects.all()
    categories = Report.objects.values('category').annotate(count=Count('id')).order_by('-count')

    context = {
        'reports':          reports,
        'total_reports':    reports.count(),
        'total_reported':   reports.filter(status='REPORTED').count(),
        'total_verified':   reports.filter(status='VERIFIED').count(),
        'total_in_progress': reports.filter(status='IN_PROGRESS').count(),
        'total_resolved':   reports.filter(status='RESOLVED').count(),
        'categories':       list(categories),
    }
    return render(request, 'reports_list.html', context)


def create_report(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        location    = request.POST.get('location', '').strip()
        category    = request.POST.get('category', 'Lainnya').strip() or 'Lainnya'
        description = request.POST.get('description', '').strip()

        if title:
            Report.objects.create(
                title=title,
                location=location,
                category=category,
                description=description,
                reporter=request.user if request.user.is_authenticated else None,
                status='REPORTED'
            )
            messages.success(request, 'Laporan berhasil dibuat!')
        return redirect('dashboard:dashboard')
    return render(request, 'add_report.html')


@_admin_required
def verify_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'VERIFIED'
    report.save()
    messages.info(request, f'Laporan "{report.title}" telah diverifikasi.')
    return redirect('main_app:reports_list')


@_admin_required
def progress_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'IN_PROGRESS'
    report.save()
    messages.warning(request, f'Laporan "{report.title}" sedang dalam pengerjaan.')
    return redirect('main_app:reports_list')


@_admin_required
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = 'RESOLVED'
    report.save()
    messages.success(request, f'Laporan "{report.title}" selesai ditangani.')
    return redirect('main_app:reports_list')


@_admin_required
def update_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        report.title    = request.POST.get('title', report.title)
        report.location = request.POST.get('location', report.location)
        report.save()
        messages.success(request, 'Data laporan berhasil diperbarui.')
        return redirect('main_app:reports_list')
    return render(request, 'update_report.html', {'report': report})


@_admin_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    messages.error(request, 'Laporan telah dihapus secara permanen.')
    return redirect('main_app:reports_list')


# ---------------------------------------------------------------------------
# AJAX / JSON API endpoints (Lab 7-9)
# ---------------------------------------------------------------------------

def search_reports(request):
    """Live search: GET /main/search/?q=<query>"""
    query = request.GET.get('q', '').strip()
    qs = (
        Report.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        ) if query else Report.objects.all()
    )
    data = list(qs.order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:20])
    return JsonResponse(data, safe=False)


def report_detail(request, report_id):
    """Detail modal: GET /main/detail/<id>/"""
    report = get_object_or_404(Report, id=report_id)
    return JsonResponse({
        'id':          report.id,
        'title':       report.title,
        'location':    report.location,
        'category':    report.category,
        'status':      report.status,
        'description': report.description,
    })


# ---------------------------------------------------------------------------
# Class-based Dashboard (Lab 7)
# ---------------------------------------------------------------------------

class DashboardView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs  = Report.objects
        ctx.update({
            'total_reports':     qs.count(),
            'total_reported':    qs.filter(status='REPORTED').count(),
            'total_verified':    qs.filter(status='VERIFIED').count(),
            'total_in_progress': qs.filter(status='IN_PROGRESS').count(),
            'total_resolved':    qs.filter(status='RESOLVED').count(),
        })
        return ctx


# ---------------------------------------------------------------------------
# API endpoints untuk chart dashboard
# ---------------------------------------------------------------------------

def api_status_statistics(request):
    qs = Report.objects
    return JsonResponse({
        'REPORTED':    qs.filter(status='REPORTED').count(),
        'VERIFIED':    qs.filter(status='VERIFIED').count(),
        'IN_PROGRESS': qs.filter(status='IN_PROGRESS').count(),
        'RESOLVED':    qs.filter(status='RESOLVED').count(),
    })


def api_category_statistics(request):
    data = {
        item['category']: item['count']
        for item in Report.objects.values('category').annotate(count=Count('id'))
    }
    return JsonResponse(data)


def api_latest_reported(request):
    qs = Report.objects.filter(status='REPORTED').order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    return JsonResponse(list(qs), safe=False)


def api_latest_resolved(request):
    qs = Report.objects.filter(status='RESOLVED').order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    return JsonResponse(list(qs), safe=False)


def api_search_reports(request):
    query = request.GET.get('q', '').strip()
    qs = (
        Report.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        ) if query else Report.objects.all()
    )
    return JsonResponse(
        list(qs.order_by('-id').values('id', 'title', 'location', 'category', 'status')[:20]),
        safe=False,
    )


def api_report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return JsonResponse({
        'id':          report.id,
        'title':       report.title,
        'location':    report.location,
        'category':    report.category,
        'description': report.description,
        'status':      report.status,
    })
