# ⚡ Lab Session 7 - Quick Reference Cheat Sheet

## 🔗 URLs API Endpoints

```
Dashboard:
GET /main_app/dashboard/

API Endpoints:
GET /main_app/api/status-statistics/
GET /main_app/api/category-statistics/
GET /main_app/api/latest-reported/
GET /main_app/api/latest-resolved/
GET /main_app/api/search/?q=keyword
GET /main_app/api/detail/<id>/
```

---

## 💻 Backend Quick Code

### DashboardView
```python
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = Report.objects.count()
        context['total_reported'] = Report.objects.filter(status='REPORTED').count()
        return context
```

### API Endpoint Pattern
```python
def api_name(request):
    data = {...}  # Get data from DB
    return JsonResponse(data)
```

### Count By Status
```python
Report.objects.filter(status='REPORTED').count()
```

### Group By Category (Aggregation)
```python
categories = Report.objects.values('category').annotate(
    count=Count('id')
).order_by('-count')
```

### Complex Query (Q objects)
```python
Report.objects.filter(
    Q(title__icontains=q) |
    Q(location__icontains=q) |
    Q(category__icontains=q)
)
```

---

## 🎨 Frontend Quick Code

### Fetch API Pattern
```javascript
async function fetchData() {
    try {
        const response = await fetch('/main_app/api/status-statistics/');
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}
```

### Debounce Function
```javascript
const debouncedFunc = debounce(async (query) => {
    const results = await searchReports(query);
}, 300);

input.addEventListener('input', (e) => debouncedFunc(e.target.value));
```

### Chart.js Doughnut
```javascript
new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['A', 'B', 'C'],
        datasets: [{
            data: [1, 2, 3],
            backgroundColor: ['#FF0000', '#00FF00', '#0000FF']
        }]
    }
});
```

### Chart.js Bar
```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['X', 'Y', 'Z'],
        datasets: [{
            label: 'Count',
            data: [10, 20, 30]
        }]
    },
    options: {
        indexAxis: 'y'  // Horizontal
    }
});
```

### Event Delegation
```javascript
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('btn-class')) {
        // Handle click
    }
});
```

### DOMContentLoaded
```javascript
document.addEventListener('DOMContentLoaded', async () => {
    // Init code here
    await renderChart();
    setupEvents();
});
```

### Render List
```javascript
let html = '';
reports.forEach(r => {
    html += `<div>${r.title}</div>`;
});
container.innerHTML = html;
```

### Modal Bootstrap 5
```javascript
const modal = new bootstrap.Modal(document.getElementById('modal'));
modal.show();
modal.hide();
```

---

## 🐛 Common Errors & Solutions

| Error | Solution |
|-------|----------|
| Template not found | Check TEMPLATES['APP_DIRS'] = True |
| Chart blank | Check browser console for errors |
| API 404 | Verify URL in urls.py |
| Fetch fails | Check endpoint & URL path |
| Event not triggered | Use event delegation or DOMContentLoaded |
| Static files 404 | Run `collectstatic` or check STATIC_URL |
| Modal not showing | Check Bootstrap version (use 5) |
| Debounce too fast/slow | Adjust delay (default 300ms) |

---

## ✅ Testing Checklist

- [ ] View accessible: `localhost:8000/main_app/dashboard/`
- [ ] API endpoint 1: `/main_app/api/status-statistics/`
- [ ] API endpoint 2: `/main_app/api/category-statistics/`
- [ ] Charts render: Both charts visible
- [ ] Search works: Type & see results
- [ ] Modal works: Click detail button
- [ ] No console errors: F12 → Console
- [ ] No network errors: F12 → Network

---

## 📱 File Locations

```
templates/dashboard.html          ← Template
static/js/dashboard.js            ← JavaScript
main_app/views.py                 ← Backend logic
main_app/urls.py                  ← URL routing
templates/base.html               ← Base template
```

---

## 🔑 Key Imports

```python
# views.py
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.http import JsonResponse

# models.py
from django.db import models
```

```html
<!-- dashboard.html -->
{% extends 'base.html' %}
{% load static %}
{% block content %}
{% endblock %}
{% block extra_js %}
{% endblock %}
```

```javascript
// dashboard.js
// Fetch
await fetch(url)

// Chart.js
new Chart(ctx, {...})

// Events
document.addEventListener('click', ...)
document.getElementById('id').addEventListener(...)
```

---

## 🚀 Setup Commands

```bash
# Start server
python manage.py runserver

# Create app (if needed)
python manage.py startapp main_app

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate

# Collect static
python manage.py collectstatic
```

---

## 🎯 Implementation Steps (Quick)

1. **Update views.py**: Add imports + functions
2. **Update urls.py**: Add URL patterns
3. **Update base.html**: Add extra_js block
4. **Create dashboard.html**: Copy template
5. **Create dashboard.js**: Copy script
6. **Test**: Run server & visit endpoints

---

## 📊 Data Structure Examples

### Status Statistics API
```json
{
    "REPORTED": 5,
    "VERIFIED": 3,
    "IN_PROGRESS": 2,
    "RESOLVED": 4
}
```

### Category Statistics API
```json
{
    "Pothole": 5,
    "Infrastructure": 3,
    "Other": 2
}
```

### Latest Reports API
```json
[
    {
        "id": 1,
        "title": "Jalan Rusak",
        "location": "Jl. Merdeka",
        "category": "Pothole",
        "status": "REPORTED"
    }
]
```

### Detail API
```json
{
    "id": 1,
    "title": "Jalan Rusak di Jl. Merdeka",
    "location": "Jl. Merdeka No.10",
    "category": "Pothole",
    "description": "Jalan berlubang besar...",
    "status": "REPORTED"
}
```

---

## ⚙️ Settings Required

```python
# settings.py
INSTALLED_APPS = [..., 'main_app']
TEMPLATES = [{
    'APP_DIRS': True,
    ...
}]
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## 🔍 Debug Tips

```javascript
// Console logging
console.log('Data:', data);
console.error('Error:', error);
console.table(array);

// Check element exists
if (element) { ... }

// Verify API response
fetch(url).then(r => console.log(r.json()))

// Check Chart instance
console.log(statusChart);
```

```bash
# Terminal debugging
python manage.py shell
>>> from main_app.models import Report
>>> Report.objects.filter(status='REPORTED').count()
>>> Report.objects.values('category').annotate(Count('id'))
```

---

## 📦 CDN Links

```html
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>

<!-- Bootstrap 5 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 🎬 Common Workflow

```
1. Check browser → http://localhost:8000/main_app/dashboard/
2. Open DevTools → F12
3. Check Console → for errors
4. Check Network → for API calls
5. Check Elements → for HTML structure
6. Modify code → back to step 1
```

---

## 💾 File Update Summary

| File | Action | Lines |
|------|--------|-------|
| views.py | Update | +220 |
| urls.py | Update | +6 |
| base.html | Update | +1 |
| dashboard.html | Create | +210 |
| dashboard.js | Create | +650 |

---

## ⏱️ Time Estimates

- Setup: 5 menit
- Implementation: 10-15 menit
- Testing: 5-10 menit
- Debugging: 5-10 menit
- **Total: 25-50 menit**

---

## 🎓 Key Concepts Summary

| Konsep | Letak | Tujuan |
|--------|-------|--------|
| TemplateView | views.py | Render template dengan context |
| JSON API | views.py | Return data untuk frontend |
| Fetch API | dashboard.js | Get data dari backend |
| async/await | dashboard.js | Handle async operations |
| Debouncing | dashboard.js | Rate limit API calls |
| Event Delegation | dashboard.js | Efficient event handling |
| Chart.js | dashboard.html | Visualize data |

---

## 📞 Quick Support

**Error dengan chart?**
→ Check browser console, verify data format

**API tidak working?**
→ Check urls.py, verify URL path

**Search lambat?**
→ Increase debounce delay (300ms → 500ms)

**Modal tidak muncul?**
→ Check Bootstrap 5 import, verify modal ID

**Static files missing?**
→ Run collectstatic, check STATIC_URL

---

**🚀 Ready to code! Good luck!**

*Print this for reference during coding session*

