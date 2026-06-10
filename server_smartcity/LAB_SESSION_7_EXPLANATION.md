# Lab Session 7: Dashboard Interaktif dengan Django & Chart.js

## 📋 Ringkasan Fitur
Implementasi dashboard lengkap untuk visualisasi laporan publik dengan:
- **Backend**: Class-Based View (TemplateView) dan JSON API endpoints
- **Frontend**: Chart.js untuk visualisasi, Fetch API untuk data, Live Search dengan debouncing
- **Interaktif**: Modal detail laporan, Event delegation, DOMContentLoaded

---

## 🏗️ STRUKTUR PROJECT

```
main_app/
├── models.py              # ✅ Model Report (sudah ada)
├── views.py              # ✅ Views & API endpoints (sudah diupdate)
├── urls.py               # ✅ URL routing (sudah diupdate)
│
templates/
├── base.html             # ✅ Base template (sudah diupdate)
├── dashboard.html        # ✅ Dashboard template (baru)
│
static/
└── js/
    └── dashboard.js      # ✅ Dashboard JavaScript (baru)
```

---

## 📝 PENJELASAN KODE

### 1️⃣ BACKEND - views.py

#### A. Class-Based View: DashboardView (TemplateView)

```python
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
        # ... dst
        
        return context
```

**Penjelasan:**
- **TemplateView**: CBV yang sederhana untuk render template
- **template_name**: File template yang akan di-render
- **get_context_data()**: Override method untuk menambah context data
- **Context**: Mengirim data statistik ke template

**URL Access**: `/main_app/dashboard/`

---

#### B. API Endpoints untuk Statistik

##### 1. Status Statistics
```python
def api_status_statistics(request):
    """
    Mengembalikan count laporan per status
    Response: {'REPORTED': 5, 'VERIFIED': 3, 'IN_PROGRESS': 2, 'RESOLVED': 4}
    """
    statistics = {
        'REPORTED': Report.objects.filter(status='REPORTED').count(),
        'VERIFIED': Report.objects.filter(status='VERIFIED').count(),
        'IN_PROGRESS': Report.objects.filter(status='IN_PROGRESS').count(),
        'RESOLVED': Report.objects.filter(status='RESOLVED').count(),
    }
    return JsonResponse(statistics)
```

**URL Access**: `/main_app/api/status-statistics/`

---

##### 2. Category Statistics
```python
def api_category_statistics(request):
    """
    Mengembalikan count laporan per kategori
    Menggunakan aggregation dengan Count()
    Response: {'Infrastructure': 5, 'Pothole': 3, ...}
    """
    categories = Report.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    statistics = {item['category']: item['count'] for item in categories}
    return JsonResponse(statistics)
```

**Penjelasan**:
- **values('category')**: Group by kategori
- **annotate(count=Count('id'))**: Hitung jumlah laporan per kategori
- **order_by('-count')**: Urut dari terbanyak ke terendah

**URL Access**: `/main_app/api/category-statistics/`

---

##### 3. Latest Reported (5 laporan terbaru status REPORTED)
```python
def api_latest_reported(request):
    """
    5 laporan terbaru dengan status REPORTED
    Response: [
        {'id': 1, 'title': '...', 'location': '...', 'category': '...', 'status': 'REPORTED'},
        ...
    ]
    """
    reports = Report.objects.filter(
        status='REPORTED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)
```

**Penjelasan**:
- **filter(status='REPORTED')**: Filter hanya laporan status REPORTED
- **order_by('-id')**: Urut dari ID terbesar (terbaru)
- **values()**: Select hanya field tertentu
- **[:5]**: Ambil 5 laporan teratas

**URL Access**: `/main_app/api/latest-reported/`

---

##### 4. Latest Resolved (5 laporan terbaru status RESOLVED)
```python
def api_latest_resolved(request):
    """
    5 laporan terbaru dengan status RESOLVED
    """
    reports = Report.objects.filter(
        status='RESOLVED'
    ).order_by('-id').values(
        'id', 'title', 'location', 'category', 'status'
    )[:5]
    
    return JsonResponse(list(reports), safe=False)
```

**URL Access**: `/main_app/api/latest-resolved/`

---

#### C. API Endpoint untuk Live Search
```python
def api_search_reports(request):
    """
    Live search laporan
    Query: /main_app/api/search/?q=jalan
    Response: Array laporan yang match
    """
    query = request.GET.get('q', '')
    
    # Validasi: query minimal 2 karakter
    if len(query) < 2:
        return JsonResponse([], safe=False)
    
    # Cari di title, location, atau category
    reports = Report.objects.filter(
        Q(title__icontains=query) |
        Q(location__icontains=query) |
        Q(category__icontains=query)
    ).values('id', 'title', 'location', 'category', 'status').order_by('-id')[:10]
    
    return JsonResponse(list(reports), safe=False)
```

**Penjelasan**:
- **Q()**: Complex query dengan OR logic
- **icontains**: Case-insensitive search
- **[:10]**: Batasi hasil max 10 item
- **Validasi**: Minimal 2 karakter untuk mengurangi server load

**URL Access**: `/main_app/api/search/?q=keyword`

---

#### D. API Endpoint untuk Detail Laporan
```python
def api_report_detail(request, report_id):
    """
    Detail laporan berdasarkan ID
    Response: {
        'id': 1,
        'title': '...',
        'location': '...',
        'category': '...',
        'description': '...',
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
```

**URL Access**: `/main_app/api/detail/<int:report_id>/`

---

### 2️⃣ FRONTEND - dashboard.html

Template menggunakan:
- **Bootstrap 5** untuk styling
- **Chart.js CDN** untuk charts
- **Static JS** untuk logic interaktif

**Struktur**:
1. **Page Title**: Header dan informasi lab
2. **Statistics Cards**: 4 card menampilkan total laporan per status
3. **Charts Section**:
   - Doughnut Chart (Status)
   - Bar Chart (Kategori)
4. **Live Search**: Input untuk pencarian real-time
5. **Latest Reports**: 2 section untuk REPORTED dan RESOLVED
6. **Modal**: Detail laporan

**Important Blocks**:
```html
{% block extra_js %}
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>

<!-- Dashboard Script -->
<script src="{% static 'js/dashboard.js' %}"></script>
{% endblock %}
```

---

### 3️⃣ FRONTEND - JavaScript (dashboard.js)

#### A. Debounce Function
```javascript
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}
```

**Kegunaan**:
- Mengurangi frequency pemanggilan API saat user mengetik
- Delay 300ms untuk wait sampai user selesai mengetik
- Mencegah request berlebihan ke server

**Contoh**:
```javascript
// Tanpa debounce: 5 karakter = 5 API calls
// Dengan debounce: 5 karakter = 1 API call (setelah 300ms)
```

---

#### B. Fetch API Functions
```javascript
async function fetchStatusStatistics() {
    const response = await fetch('/main_app/api/status-statistics/');
    return await response.json();
}

async function fetchCategoryStatistics() {
    const response = await fetch('/main_app/api/category-statistics/');
    return await response.json();
}

async function fetchLatestReported() {
    const response = await fetch('/main_app/api/latest-reported/');
    return await response.json();
}

async function fetchLatestResolved() {
    const response = await fetch('/main_app/api/latest-resolved/');
    return await response.json();
}

async function searchReports(query) {
    const response = await fetch(
        `/main_app/api/search/?q=${encodeURIComponent(query)}`
    );
    return await response.json();
}

async function fetchReportDetail(reportId) {
    const response = await fetch(`/main_app/api/detail/${reportId}/`);
    return await response.json();
}
```

**Kegunaan**:
- Mengambil data dari backend tanpa reload
- **async/await**: Syntax modern untuk handling async operations
- **Error handling**: Try-catch untuk error gracefully

---

#### C. Chart Rendering Functions

##### Doughnut Chart (Status)
```javascript
async function renderStatusChart() {
    const data = await fetchStatusStatistics();
    
    // Destroy existing chart jika ada
    if (statusChart) {
        statusChart.destroy();
    }

    const colors = {
        'REPORTED': '#FFC107',
        'VERIFIED': '#17A2B8',
        'IN_PROGRESS': '#007BFF',
        'RESOLVED': '#28A745',
    };

    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: labels.map(label => colors[label]),
            }]
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}
```

**Fitur**:
- Tampilkan percentage di tooltip
- Warna sesuai status
- Destroy chart lama untuk prevent memory leak

---

##### Bar Chart (Kategori)
```javascript
async function renderCategoryChart() {
    const data = await fetchCategoryStatistics();
    
    if (categoryChart) {
        categoryChart.destroy();
    }

    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Jumlah Laporan',
                data: Object.values(data),
                backgroundColor: [...colors],
            }]
        },
        options: {
            indexAxis: 'y',  // Horizontal bar
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                    }
                }
            }
        }
    });
}
```

**Fitur**:
- Horizontal bar chart (indexAxis: 'y')
- Warna berbeda untuk setiap bar
- Grid step size = 1 untuk bilangan bulat

---

#### D. Render List Functions
```javascript
function renderReportList(reports, containerId) {
    const container = document.getElementById(containerId);
    
    if (reports.length === 0) {
        container.innerHTML = '<p class="text-muted">Belum ada laporan</p>';
        return;
    }

    let html = '';
    reports.forEach(report => {
        html += `
            <div class="list-group-item">
                <h6>${report.title}</h6>
                <p>${report.location}</p>
                <button class="detail-btn" data-report-id="${report.id}">Detail</button>
            </div>
        `;
    });

    container.innerHTML = html;
}
```

**Kegunaan**:
- Mengubah array data menjadi HTML
- Template literals untuk string interpolation
- data-report-id untuk menyimpan report ID

---

#### E. Modal Functions
```javascript
async function showDetailModal(reportId) {
    const report = await fetchReportDetail(reportId);
    
    // Update modal content dengan report data
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
        <div>
            <label>Judul:</label>
            <p>${report.title}</p>
            <label>Lokasi:</label>
            <p>${report.location}</p>
            <label>Deskripsi:</label>
            <p>${report.description}</p>
        </div>
    `;

    // Tampilkan modal menggunakan Bootstrap 5
    const modal = new bootstrap.Modal(document.getElementById('detailModal'));
    modal.show();
}
```

**Kegunaan**:
- Menampilkan detail laporan di modal
- Dynamic content berdasarkan report ID
- Bootstrap Modal API

---

#### F. Event Listeners & Initialization

##### Live Search dengan Debouncing
```javascript
const debouncedSearch = debounce(async function (query) {
    if (query.length < 2) {
        document.getElementById('searchResults').innerHTML = '';
        return;
    }

    const results = await searchReports(query);
    renderSearchResults(results);
}, 300); // Delay 300ms

document.getElementById('searchInput').addEventListener('input', function (e) {
    const query = e.target.value.trim();
    debouncedSearch(query);
});
```

---

##### Event Delegation untuk Detail Button
```javascript
document.addEventListener('click', function (e) {
    // Cek apakah element yang diklik adalah detail-btn
    if (e.target.classList.contains('detail-btn')) {
        e.preventDefault();
        const reportId = e.target.getAttribute('data-report-id');
        if (reportId) {
            showDetailModal(reportId);
        }
    }
});
```

**Kegunaan**:
- **Event Delegation**: Attach listener ke parent element
- Handle click pada dinamis button tanpa attach multiple listeners
- Lebih efisien untuk element yang dibuat dynamically

---

##### DOMContentLoaded untuk Inisialisasi
```javascript
document.addEventListener('DOMContentLoaded', async function () {
    console.log('Dashboard initialized');

    // 1. Render Charts
    await renderStatusChart();
    await renderCategoryChart();

    // 2. Load Latest Reports
    const latestReported = await fetchLatestReported();
    const latestResolved = await fetchLatestResolved();
    
    renderReportList(latestReported, 'latestReportedList');
    renderReportList(latestResolved, 'latestResolvedList');

    // 3. Setup Event Listeners
    // ...
});
```

**Kegunaan**:
- Menunggu DOM siap sebelum execute script
- Prevent error: element belum ter-load
- Organize initialization logic

---

## 🔄 ALUR DATA

```
USER AKSES /main_app/dashboard/
    ↓
DashboardView render dashboard.html
    ↓
Template load, trigger DOMContentLoaded di JS
    ↓
fetchStatusStatistics() → API /main_app/api/status-statistics/
fetchCategoryStatistics() → API /main_app/api/category-statistics/
fetchLatestReported() → API /main_app/api/latest-reported/
fetchLatestResolved() → API /main_app/api/latest-resolved/
    ↓
Backend return JSON data
    ↓
Frontend render Charts & Lists (tanpa reload)
    ↓
User input di search box
    ↓
debouncedSearch(query) trigger setelah 300ms
    ↓
searchReports(query) → API /main_app/api/search/?q=...
    ↓
Backend return hasil search
    ↓
Frontend render search results dinamically
    ↓
User klik "Detail" button
    ↓
Event Delegation trigger showDetailModal()
    ↓
fetchReportDetail(reportId) → API /main_app/api/detail/{id}/
    ↓
Backend return detail laporan
    ↓
Frontend tampilkan modal dengan detail
```

---

## ✅ CHECKLIST IMPLEMENTASI

- [x] Class-Based View (TemplateView) untuk dashboard
- [x] API endpoint untuk status statistics
- [x] API endpoint untuk category statistics
- [x] API endpoint untuk 5 laporan terbaru REPORTED
- [x] API endpoint untuk 5 laporan terbaru RESOLVED
- [x] API endpoint untuk live search
- [x] API endpoint untuk detail laporan
- [x] Doughnut Chart (Status) menggunakan Chart.js
- [x] Bar Chart (Kategori) menggunakan Chart.js
- [x] Fetch API untuk mengambil data tanpa reload
- [x] Live Search dengan Debouncing
- [x] Detail Modal dengan Event Delegation
- [x] DOMContentLoaded untuk inisialisasi
- [x] PEP8 compliant code
- [x] Dokumentasi lengkap

---

## 🚀 CARA MENGGUNAKAN

1. **Akses Dashboard**:
   ```
   http://localhost:8000/main_app/dashboard/
   ```

2. **Lihat Charts**:
   - Doughnut chart menampilkan distribusi status
   - Bar chart menampilkan distribusi kategori

3. **Live Search**:
   - Ketik di search box (minimum 2 karakter)
   - Hasil tampil real-time tanpa reload

4. **Lihat Detail**:
   - Klik tombol "Detail" pada laporan
   - Modal tampil dengan informasi lengkap

---

## 📚 REFERENCE

- [Django Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [Fetch API MDN](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Event Delegation MDN](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#event_delegation)
- [PEP 8 Style Guide](https://pep8.org/)

---

## 📝 CATATAN

- Semua kode mengikuti standar PEP8
- Debouncing delay: 300ms (dapat disesuaikan)
- Search minimum query: 2 karakter
- Max search results: 10 item
- Max latest reports: 5 item per endpoint
- Browser compatibility: Modern browsers dengan ES6+ support

