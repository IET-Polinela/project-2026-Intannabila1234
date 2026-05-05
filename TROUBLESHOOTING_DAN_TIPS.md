# Lab Session 7: Troubleshooting & Tips Penting

## 🔧 Troubleshooting

### 1. Error: Template Not Found `dashboard.html`

**Gejala**:
```
TemplateDoesNotExist at /main_app/dashboard/
dashboard.html
```

**Solusi**:
- ✅ Pastikan file `dashboard.html` berada di folder `templates/`
- ✅ Pastikan `'APP_DIRS': True` di settings.py
- ✅ Pastikan app `main_app` di `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',  # ✅ Tambahkan jika belum
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # ✅ Set ke True
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

### 2. Error: Chart Not Rendering (Blank Canvas)

**Gejala**:
- Canvas element ada, tapi chart tidak muncul

**Penyebab & Solusi**:

**A. Chart.js tidak ter-load**
```html
<!-- ✅ Tambahkan di atas script dashboard.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
<script src="{% static 'js/dashboard.js' %}"></script>
```

**B. Canvas element tidak ditemukan**
```javascript
// ✅ Cek apakah element ada
const ctx = document.getElementById('statusChart');
console.log(ctx); // Harus ada element, bukan null
```

**C. Data tidak loading**
```javascript
// ✅ Check di console
const data = await fetchStatusStatistics();
console.log(data); // Harus ada data, bukan null/empty
```

---

### 3. Error: API 404 Not Found

**Gejala**:
```
GET http://localhost:8000/main_app/api/status-statistics/ 404 (Not Found)
```

**Penyebab & Solusi**:

**A. URL belum di-register di urls.py**
```python
# ✅ Pastikan ada di main_app/urls.py
urlpatterns = [
    path('api/status-statistics/', views.api_status_statistics, name='api_status_stats'),
    # ... endpoint lainnya
]
```

**B. URL prefix salah di fetch**
```javascript
// ❌ SALAH - Sesuaikan dengan URL di urls.py
await fetch('/main_app/api/status-statistics/');

// ✅ BENAR - URL harus match dengan path di urls.py
await fetch('/main_app/api/status-statistics/');
```

**C. Main project URLs tidak include main_app URLs**
```python
# ✅ Pastikan di npm24782077_iet_2026/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_app/', include('main_app.urls')),  # ✅ Include ini
]
```

---

### 4. Error: TypeError - "Cannot read property 'classList'"

**Gejala**:
```
TypeError: Cannot read property 'classList' of null
```

**Penyebab**: Element tidak ditemukan

**Solusi**:
```javascript
// ❌ SALAH
const btn = document.getElementById('searchInput');
btn.addEventListener('click', ...);

// ✅ BENAR - Cek dulu apakah element ada
const btn = document.getElementById('searchInput');
if (btn) {
    btn.addEventListener('click', ...);
}
```

---

### 5. Error: CORS (Cross-Origin Request Blocked)

**Gejala**:
```
Access to XMLHttpRequest at 'http://...' from origin 'http://...' 
has been blocked by CORS policy
```

**Solusi**:
Biasanya tidak terjadi untuk same-origin requests. Jika terjadi:

```python
# ✅ settings.py - Tambahkan CORS headers
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Atau install django-cors-headers:
# pip install django-cors-headers
```

---

### 6. Error: Static Files Not Loading

**Gejala**:
```
GET http://localhost:8000/static/js/dashboard.js 404 (Not Found)
```

**Solusi**:

```python
# ✅ settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ✅ Run di terminal
python manage.py collectstatic
```

**Atau di template**:
```html
{% load static %}
<script src="{% static 'js/dashboard.js' %}"></script>
```

---

### 7. Error: ImportError - "cannot import name 'TemplateView'"

**Gejala**:
```
ImportError: cannot import name 'TemplateView' from 'django.views.generic'
```

**Solusi**:
```python
# ✅ views.py - Import yang benar
from django.views.generic import TemplateView
```

---

### 8. Error: "Q" object not defined

**Gejala**:
```
NameError: name 'Q' is not defined
```

**Solusi**:
```python
# ✅ views.py - Import Q
from django.db.models import Count, Q
```

---

## 💡 Tips Penting

### 1. Gunakan Console Browser untuk Debug
```javascript
// ✅ Buka Developer Tools (F12) → Console
console.log('Data:', data);
console.error('Error:', error);
```

### 2. Test API Endpoints di Browser
```
Langsung akses di browser:
- http://localhost:8000/main_app/api/status-statistics/
- http://localhost:8000/main_app/api/category-statistics/
- http://localhost:8000/main_app/api/search/?q=test
```

### 3. Gunakan Network Tab untuk Monitoring Requests
- Buka Developer Tools (F12) → Network tab
- Lihat request/response dari API
- Cek status code, response body, headers

### 4. Debouncing Setting
```javascript
// ✅ 300ms - Recommended (balance antara responsiveness & efficiency)
const debouncedSearch = debounce(searchFunction, 300);

// Bisa disesuaikan:
// - 100ms: Lebih responsif, tapi lebih banyak API calls
// - 500ms: Lebih efisien, tapi terasa lambat
```

### 5. Search Validation
```python
# ✅ Minimal 2 karakter untuk valid search
if len(query) < 2:
    return JsonResponse([], safe=False)
```

### 6. Limit Results
```python
# ✅ Batasi hasil untuk efficiency
reports = Report.objects.filter(...).order_by('-id')[:10]  # Max 10
```

### 7. Error Handling di JavaScript
```javascript
// ✅ Always use try-catch
try {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
} catch (error) {
    console.error('Error:', error);
    return null;
}
```

### 8. Event Delegation untuk Dynamic Elements
```javascript
// ✅ Attach ke parent, cek target
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('detail-btn')) {
        // Handle click
    }
});

// ❌ JANGAN - Attach ke setiap element
reports.forEach(report => {
    document.querySelector(`#btn-${report.id}`).addEventListener('click', ...);
});
```

### 9. Modal Bootstrap 5 Syntax
```javascript
// ✅ Bootstrap 5
const modal = new bootstrap.Modal(document.getElementById('detailModal'));
modal.show();
modal.hide();

// ❌ SALAH - Bootstrap 4 syntax
$('#detailModal').modal('show');
```

### 10. Template Tags Django
```html
<!-- ✅ BENAR - Django template syntax -->
<a href="{% url 'main_app:dashboard' %}">Dashboard</a>
<script src="{% static 'js/dashboard.js' %}"></script>

<!-- ❌ SALAH -->
<a href="/main_app/dashboard/">Dashboard</a>
<script src="/static/js/dashboard.js"></script>
```

---

## 📋 Checklist Sebelum Submit

- [ ] Semua file sudah dibuat:
  - [ ] main_app/views.py (sudah diupdate)
  - [ ] main_app/urls.py (sudah diupdate)
  - [ ] templates/dashboard.html (baru)
  - [ ] templates/base.html (sudah diupdate)
  - [ ] static/js/dashboard.js (baru)

- [ ] URLs accessible:
  - [ ] `/main_app/dashboard/` → Dashboard tampil
  - [ ] `/main_app/api/status-statistics/` → JSON response
  - [ ] `/main_app/api/category-statistics/` → JSON response

- [ ] Fitur berfungsi:
  - [ ] Charts render dengan data
  - [ ] Live search bekerja
  - [ ] Detail modal tampil saat klik tombol
  - [ ] Debouncing bekerja (cek Network tab)

- [ ] Browser Console:
  - [ ] Tidak ada error messages
  - [ ] Tidak ada warning penting

- [ ] Code Quality:
  - [ ] PEP8 compliant
  - [ ] Proper indentation
  - [ ] Meaningful variable names
  - [ ] Comments/docstrings

---

## 🧪 Manual Testing

### 1. Test Dashboard View
```bash
1. Navigate ke http://localhost:8000/main_app/dashboard/
2. Lihat apakah page load tanpa error
3. Lihat statistics cards menampilkan angka
4. Lihat charts render dengan data
```

### 2. Test API Endpoints
```bash
1. curl http://localhost:8000/main_app/api/status-statistics/
2. curl http://localhost:8000/main_app/api/category-statistics/
3. curl http://localhost:8000/main_app/api/latest-reported/
4. curl http://localhost:8000/main_app/api/search/?q=test
5. curl http://localhost:8000/main_app/api/detail/1/
```

### 3. Test Live Search
```bash
1. Type di search box (2+ karakter)
2. Lihat hasil di search results
3. Buka Browser Network tab
4. Verifikasi hanya 1 request setiap 300ms (debouncing)
```

### 4. Test Detail Modal
```bash
1. Klik tombol "Detail" di laporan
2. Modal tampil dengan info lengkap
3. Close modal dengan tombol "Tutup"
```

---

## 📚 References untuk Study Lebih Lanjut

- Django TemplateView: https://docs.djangoproject.com/en/stable/ref/class-based-views/base/#templateview
- Chart.js Docs: https://www.chartjs.org/docs/latest/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- Event Delegation: https://javascript.info/event-delegation
- Debouncing: https://www.freecodecamp.org/news/deboucing-and-throttling-in-javascript/
- PEP 8: https://www.python.org/dev/peps/pep-0008/

---

## ✨ Tips Bonus

### Refresh Charts Secara Periodic
```javascript
// Uncomment di bagian akhir dashboard.js untuk auto-refresh setiap 30 detik
setInterval(async () => {
    await renderStatusChart();
    await renderCategoryChart();
}, 30000);
```

### Tambah Loading Indicator
```html
<!-- Di dashboard.html -->
<div id="loadingSpinner" class="spinner-border" role="status" style="display:none;">
    <span class="visually-hidden">Loading...</span>
</div>
```

```javascript
// Di dashboard.js
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}
```

### Tambah Error Handling UI
```javascript
// Tampilkan error message ke user
function showError(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('body').insertBefore(alert, document.querySelector('main'));
}
```

---

## 🎯 Kesimpulan

Jika ada error yang belum tercantum:
1. Baca error message dengan teliti
2. Cek console browser (F12)
3. Cek Network tab untuk API requests
4. Cek Django error logs di terminal
5. Search error di Stack Overflow atau Django docs

**Semua fitur sudah siap! Selamat mengerjakan Lab Session 7! 🚀**

