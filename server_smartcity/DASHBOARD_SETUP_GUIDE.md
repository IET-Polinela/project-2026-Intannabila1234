# Lab Session 7 - Dashboard Setup Complete! ✅

## 🎯 Apa yang Sudah Dibuat

### 1. ✅ App Dashboard
- **App Name**: `dashboard_24782077`
- **Status**: Created & configured

### 2. ✅ Views (views.py)
- **DashboardView** - Class-Based View (TemplateView)
- **dashboard_data** - JsonResponse API untuk statistik
- **latest_reported** - JsonResponse API untuk 5 laporan terbaru REPORTED
- **latest_resolved** - JsonResponse API untuk 5 laporan terbaru RESOLVED

### 3. ✅ URLs (urls.py)
- **Dashboard Main**: `/dashboard/` → DashboardView
- **API Data**: `/dashboard/api/data/` → dashboard_data
- **API Reported**: `/dashboard/api/latest-reported/` → latest_reported
- **API Resolved**: `/dashboard/api/latest-resolved/` → latest_resolved

### 4. ✅ Template (index.html)
- **Location**: `templates/dashboard/index.html`
- **Features**: Statistics cards, charts, latest reports lists

### 5. ✅ Configuration
- **INSTALLED_APPS**: `dashboard_24782077` sudah ditambahkan ke settings.py
- **URL Include**: Dashboard URL sudah di-include di project urls.py

---

## 🔴 Penjelasan Error 404: "Page not found /dashboard"

### **Penyebab Error 404**

Error 404 terjadi ketika:

1. **App belum di-register di INSTALLED_APPS**
   ```python
   # ❌ SALAH - App tidak terdaftar
   INSTALLED_APPS = [
       'django.contrib.admin',
       'main_app.apps.MainAppConfig',
       'contacts.apps.ContactsConfig',
       # dashboard_24782077 TIDAK ada di sini!
   ]
   
   # ✅ BENAR - App sudah terdaftar
   INSTALLED_APPS = [
       'django.contrib.admin',
       'main_app.apps.MainAppConfig',
       'contacts.apps.ContactsConfig',
       'dashboard_24782077.apps.Dashboard24782077Config',  # ← DITAMBAHKAN
   ]
   ```

2. **URL Dashboard belum di-include di project urls.py**
   ```python
   # ❌ SALAH - Dashboard URL tidak ter-include
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('main/', include('main_app.urls')),
       # dashboard tidak ada di sini!
   ]
   
   # ✅ BENAR - Dashboard URL sudah ter-include
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('main/', include('main_app.urls')),
       path('dashboard/', include('dashboard_24782077.urls')),  # ← DITAMBAHKAN
   ]
   ```

3. **Template tidak ditemukan pada lokasi yang benar**
   ```python
   # ❌ SALAH
   template_name = 'index.html'  # Django akan cari di root templates/
   
   # ✅ BENAR
   template_name = 'dashboard/index.html'  # Django cari di templates/dashboard/
   ```

---

## 🧠 Cara Django Resolve URL

```
User akses: http://localhost:8000/dashboard/
    ↓
Django buka urls.py (project)
    ↓
Cari pattern yang match '/dashboard/'
    ↓
Found: path('dashboard/', include('dashboard_24782077.urls'))
    ↓
Django buka dashboard_24782077/urls.py
    ↓
Cari pattern yang match '/' (sisa URL setelah /dashboard/)
    ↓
Found: path('', views.DashboardView.as_view(), name='index')
    ↓
Execute DashboardView
    ↓
Load template 'dashboard/index.html'
    ↓
Send response ke browser
    ↓
✅ Success! Dashboard tampil
```

---

## 🚀 Testing Dashboard

### Step 1: Jalankan Server
```bash
python manage.py runserver
```

### Step 2: Akses URLs

**Dashboard Main:**
```
http://localhost:8000/dashboard/
```
→ Harus tampil halaman dashboard dengan 4 statistics cards

**API Endpoints:**
```
http://localhost:8000/dashboard/api/data/
```
→ Return JSON dengan status dan category stats

```
http://localhost:8000/dashboard/api/latest-reported/
```
→ Return JSON array dengan 5 laporan REPORTED terbaru

```
http://localhost:8000/dashboard/api/latest-resolved/
```
→ Return JSON array dengan 5 laporan RESOLVED terbaru

### Step 3: Browser DevTools Inspection

**Buka F12 → Network Tab**

Ketika dashboard load, Anda akan melihat:
- `GET /dashboard/` → 200 OK (main page)
- `GET /dashboard/api/data/` → 200 OK (JSON data untuk charts)
- `GET /dashboard/api/latest-reported/` → 200 OK
- `GET /dashboard/api/latest-resolved/` → 200 OK

Semua harus status 200, bukan 404.

---

## 📊 Expected Output

### Dashboard View (DashboardView)

**Context Data:**
```python
{
    'total_reports': 14,
    'reported_count': 5,
    'verified_count': 3,
    'in_progress_count': 2,
    'resolved_count': 4,
    'category_stats': [
        {'category': 'Pothole', 'count': 5},
        {'category': 'Infrastructure', 'count': 3},
        {'category': 'Other', 'count': 2},
    ]
}
```

### API Response (`/dashboard/api/data/`)

```json
{
    "status": {
        "REPORTED": 5,
        "VERIFIED": 3,
        "IN_PROGRESS": 2,
        "RESOLVED": 4
    },
    "categories": {
        "Pothole": 5,
        "Infrastructure": 3,
        "Other": 2
    },
    "total": 14
}
```

### API Response (`/dashboard/api/latest-reported/`)

```json
[
    {
        "id": 5,
        "title": "Jalan Rusak di Jl. Merdeka",
        "location": "Jl. Merdeka No.10",
        "category": "Pothole",
        "status": "REPORTED"
    },
    {
        "id": 4,
        "title": "Lampu Jalan Mati",
        "location": "Jl. Ahmad Yani",
        "category": "Infrastructure",
        "status": "REPORTED"
    }
]
```

---

## ✅ Checklist Sebelum Submit

- [ ] App `dashboard_24782077` sudah di-register di INSTALLED_APPS
- [ ] Project urls.py sudah include dashboard URLs
- [ ] Dashboard URLs di-define dengan benar di dashboard_24782077/urls.py
- [ ] DashboardView menggunakan TemplateView (CBV)
- [ ] Template berada di `templates/dashboard/index.html`
- [ ] API endpoints return JsonResponse
- [ ] Charts render dengan data dari API
- [ ] Server berjalan tanpa error
- [ ] URLs accessible:
  - [ ] `/dashboard/` → 200 OK
  - [ ] `/dashboard/api/data/` → 200 OK
  - [ ] `/dashboard/api/latest-reported/` → 200 OK
  - [ ] `/dashboard/api/latest-resolved/` → 200 OK
- [ ] Charts tampil dengan data
- [ ] Latest reports lists populate dengan data

---

## 🔍 Troubleshooting

### Error: "Page not found (404) /dashboard"

**Solution:**
1. Cek INSTALLED_APPS di settings.py → tambahkan `dashboard_24782077.apps.Dashboard24782077Config`
2. Cek project urls.py → tambahkan `path('dashboard/', include('dashboard_24782077.urls'))`
3. Restart server: `Ctrl+C` lalu `python manage.py runserver`

### Error: "TemplateDoesNotExist at /dashboard/"

**Solution:**
1. Pastikan file `templates/dashboard/index.html` ada
2. Pastikan template_name di DashboardView = `'dashboard/index.html'`
3. Check TEMPLATES['DIRS'] di settings.py → harus include `BASE_DIR / 'templates'`

### Charts tidak render / blank

**Solution:**
1. Buka F12 → Console → cek error messages
2. Check F12 → Network → pastikan API endpoints return 200 OK
3. Pastikan Chart.js CDN link benar di template
4. Check browser console → lihat fetch responses

### API endpoints return 404

**Solution:**
1. Pastikan dashboard_24782077/urls.py sudah di-create
2. Pastikan URL patterns di-define dengan benar
3. Pastikan project urls.py include dashboard URLs dengan `include()`
4. Restart server

---

## 📚 File Structure

```
project/
├── dashboard_24782077/              ← Dashboard App
│   ├── views.py                     ✅ Updated
│   ├── urls.py                      ✅ Created
│   ├── apps.py
│   ├── models.py
│   ├── admin.py
│   ├── migrations/
│   └── __init__.py
│
├── npm24782077_iet_2026/            ← Project Main
│   ├── settings.py                  ✅ Updated (INSTALLED_APPS)
│   ├── urls.py                      ✅ Updated (include dashboard)
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
│
├── templates/
│   ├── dashboard/                   ← Dashboard Templates
│   │   └── index.html               ✅ Created
│   ├── base.html
│   └── ...
│
├── main_app/                         ← Existing App
│   ├── views.py
│   ├── models.py (Report model)
│   └── ...
│
└── manage.py
```

---

## 🎓 Key Concepts

### Class-Based View (TemplateView)
```python
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context
        context['data'] = ...
        return context
```

**Keuntungan:**
- Clean & organized code
- Reusable logic
- Easy to maintain
- Follow Django best practices

### JsonResponse API
```python
def api_endpoint(request):
    data = {
        'status': {...},
        'categories': {...},
        'total': 14
    }
    return JsonResponse(data, safe=False)
```

**Keuntungan:**
- Easy to fetch di frontend dengan Fetch API
- No page reload
- Real-time data
- Suitable untuk Chart.js

### ORM Aggregation dengan annotate() & Count()
```python
categories = Report.objects.values('category').annotate(
    count=Count('id')
).order_by('-count')
```

**SQL Equivalent:**
```sql
SELECT category, COUNT(id) as count
FROM main_app_report
GROUP BY category
ORDER BY count DESC
```

---

## ✨ Lab Session 7 Requirements ✅

| Requirement | Implementation |
|---|---|
| Class-Based View (TemplateView) | ✅ `DashboardView` |
| JsonResponse API | ✅ `dashboard_data`, `latest_reported`, `latest_resolved` |
| Count Status Laporan | ✅ `status_stats` di `dashboard_data()` |
| Count Kategori Laporan | ✅ `category_stats` dengan ORM aggregation |
| Django ORM Aggregation | ✅ `values().annotate(count=Count('id'))` |
| Chart.js Visualisasi | ✅ Doughnut chart & Bar chart |
| Fetch API | ✅ async/await fetch di template |
| No page reload | ✅ Charts update via AJAX |

---

## 🎉 Dashboard Ready!

Dashboard Anda sudah lengkap dan siap untuk:
- ✅ Menampilkan statistik laporan (cards)
- ✅ Visualisasi data dengan Chart.js (doughnut & bar)
- ✅ Fetch data real-time dari API (tanpa reload)
- ✅ Menampilkan laporan terbaru (lists)

**Selamat mengerjakan Lab Session 7! 🚀**

---

**Last Updated:** April 29, 2026  
**Lab:** Session 7 - Pemrograman Internet 1  
**Program:** Teknologi Rekayasa Internet (S1)

