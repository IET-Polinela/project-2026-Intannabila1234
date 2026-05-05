# 🚀 Quick Start Guide - Lab Session 7

## ⚡ Setup Cepat (5 Menit)

### Step 1: Update `main_app/views.py`
Copy-paste imports baru di atas:
```python
from django.views.generic import TemplateView
from django.db.models import Count, Q
```

Tambah di akhir file:
```python
# Class-Based View
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = Report.objects.count()
        context['total_reported'] = Report.objects.filter(status='REPORTED').count()
        context['total_verified'] = Report.objects.filter(status='VERIFIED').count()
        context['total_in_progress'] = Report.objects.filter(status='IN_PROGRESS').count()
        context['total_resolved'] = Report.objects.filter(status='RESOLVED').count()
        return context

# API Endpoints
def api_status_statistics(request):
    return JsonResponse({
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    })

def api_category_statistics(request):
    categories = Report.objects.values('category').annotate(count=Count('id')).order_by('-count')
    return JsonResponse({item['category']: item['count'] for item in categories})

def api_latest_reported(request):
    reports = Report.objects.filter(status='REPORTED').order_by('-id').values('id', 'title', 'location', 'category', 'status')[:5]
    return JsonResponse(list(reports), safe=False)

def api_latest_resolved(request):
    reports = Report.objects.filter(status='RESOLVED').order_by('-id').values('id', 'title', 'location', 'category', 'status')[:5]
    return JsonResponse(list(reports), safe=False)

def api_search_reports(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)
    reports = Report.objects.filter(Q(title__icontains=query)|Q(location__icontains=query)|Q(category__icontains=query)).values('id', 'title', 'location', 'category', 'status').order_by('-id')[:10]
    return JsonResponse(list(reports), safe=False)

def api_report_detail(request, report_id):
    try:
        report = Report.objects.get(id=report_id)
        return JsonResponse({'id': report.id, 'title': report.title, 'location': report.location, 'category': report.category, 'description': report.description, 'status': report.status})
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
```

---

### Step 2: Update `main_app/urls.py`
Replace entire file:
```python
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/status-statistics/', views.api_status_statistics, name='api_status_stats'),
    path('api/category-statistics/', views.api_category_statistics, name='api_category_stats'),
    path('api/latest-reported/', views.api_latest_reported, name='api_latest_reported'),
    path('api/latest-resolved/', views.api_latest_resolved, name='api_latest_resolved'),
    path('api/search/', views.api_search_reports, name='api_search'),
    path('api/detail/<int:report_id>/', views.api_report_detail, name='api_detail'),
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

### Step 3: Update `templates/base.html`
Tambah sebelum `</body>`:
```html
{% block extra_js %}{% endblock %}
```

---

### Step 4: Create `templates/dashboard.html`
File sudah siap - copy dari `dashboard.html` yang sudah dibuat

---

### Step 5: Create `static/js/dashboard.js`
File sudah siap - copy dari `static/js/dashboard.js` yang sudah dibuat

---

### Step 6: Run Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/main_app/dashboard/`

---

## ✅ Verification Checklist

```bash
# 1. Test Dashboard View
curl http://localhost:8000/main_app/dashboard/

# 2. Test API Endpoints
curl http://localhost:8000/main_app/api/status-statistics/
curl http://localhost:8000/main_app/api/category-statistics/
curl http://localhost:8000/main_app/api/latest-reported/
curl http://localhost:8000/main_app/api/latest-resolved/

# 3. Test Search
curl "http://localhost:8000/main_app/api/search/?q=jalan"

# 4. Test Detail
curl http://localhost:8000/main_app/api/detail/1/
```

---

## 📝 File Summary

| File | Status | Action |
|------|--------|--------|
| `main_app/models.py` | ✅ Existing | No change |
| `main_app/views.py` | ⚠️ Update | Add new functions |
| `main_app/urls.py` | ⚠️ Update | Add new paths |
| `templates/base.html` | ⚠️ Update | Add `{% block extra_js %}` |
| `templates/dashboard.html` | 🆕 Create | New file |
| `static/js/dashboard.js` | 🆕 Create | New file |

---

## 🎯 Features Implemented

- ✅ TemplateView untuk dashboard
- ✅ 6 API endpoints (JSON)
- ✅ Doughnut Chart (Status)
- ✅ Bar Chart (Kategori)
- ✅ Live Search + Debouncing
- ✅ Detail Modal
- ✅ Event Delegation
- ✅ DOMContentLoaded

---

## 📚 Documentation Files

1. **LAB_SESSION_7_EXPLANATION.md** - Penjelasan detail tiap bagian
2. **KODE_LENGKAP_LAB7.md** - Kode lengkap untuk referensi
3. **TROUBLESHOOTING_DAN_TIPS.md** - Troubleshooting & tips
4. **README_QUICKSTART.md** - File ini

---

## 💬 Common Questions

### Q: Berapa lama implement semua ini?
**A**: 10-15 menit untuk copy-paste, 30 menit dengan debugging

### Q: Apakah perlu database migration?
**A**: Tidak, model Report sudah ada

### Q: Bagaimana kalau ada error?
**A**: Lihat `TROUBLESHOOTING_DAN_TIPS.md`

### Q: Apakah saya bisa customize?
**A**: Ya! Semuanya modular dan mudah di-customize

### Q: Bagaimana cara tambah fitur baru?
**A**: 
1. Tambah function baru di views.py
2. Register URL di urls.py
3. Call dari JavaScript dengan fetch

---

## 🚨 Important Notes

- Pastikan `INSTALLED_APPS` include `main_app`
- Pastikan `APP_DIRS: True` di TEMPLATES setting
- Pastikan static files properly configured
- Test di browser console (F12) jika ada error

---

## 🎓 Learning Outcomes

Setelah mengerjakan lab ini, Anda bisa:
- ✅ Membuat Class-Based View (TemplateView)
- ✅ Membuat JSON API endpoints
- ✅ Menggunakan Chart.js untuk visualisasi
- ✅ Menggunakan Fetch API (async/await)
- ✅ Implement Live Search dengan debouncing
- ✅ Menggunakan Event Delegation
- ✅ Membuat responsive dashboard

---

## 🔗 Next Steps

Setelah submit:
1. Add authentication check (hanya authenticated user)
2. Add export feature (CSV/PDF)
3. Add real-time updates dengan WebSocket
4. Add more charts (Pie, Line, Area)
5. Add date range filter

---

**Happy coding! 🚀 Semoga lancar mengerjakan Lab Session 7!**

