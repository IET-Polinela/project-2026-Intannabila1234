# 🏃 Run & Test Instructions - Lab Session 7

## 1️⃣ START SERVER

### Di Terminal / Command Prompt:

```bash
cd c:\Users\Lenovo\Documents\npm24782077_iet_2026

python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 29, 2026 - XX:XX:XX
Django version 4.x, Python 3.x
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Jika melihat output di atas, server berhasil jalan!**

---

## 2️⃣ ACCESS DASHBOARD

### Di Browser:

Ketik URL ini:
```
http://localhost:8000/main_app/dashboard/
```

**Expected Result:**
```
Dashboard page dengan:
├─ Header "📊 Dashboard Laporan Publik"
├─ 4 cards (Total, Reported, In Progress, Resolved)
├─ Doughnut chart (Status)
├─ Bar chart (Kategori)
├─ Search box
├─ Latest reported list
└─ Latest resolved list
```

✅ **Jika melihat ini, dashboard works!**

---

## 3️⃣ TEST API ENDPOINTS

### Test 1: Status Statistics
```
URL: http://localhost:8000/main_app/api/status-statistics/

Expected: JSON
{
    "REPORTED": 0,
    "VERIFIED": 0,
    "IN_PROGRESS": 0,
    "RESOLVED": 0
}
```

### Test 2: Category Statistics
```
URL: http://localhost:8000/main_app/api/category-statistics/

Expected: JSON
{
    "category1": 0,
    "category2": 0
}
```

### Test 3: Latest Reported
```
URL: http://localhost:8000/main_app/api/latest-reported/

Expected: JSON Array
[
    {
        "id": 1,
        "title": "...",
        "location": "...",
        "category": "...",
        "status": "REPORTED"
    }
]
```

### Test 4: Latest Resolved
```
URL: http://localhost:8000/main_app/api/latest-resolved/

Expected: JSON Array
[
    {
        "id": 1,
        "title": "...",
        "location": "...",
        "category": "...",
        "status": "RESOLVED"
    }
]
```

### Test 5: Live Search
```
URL: http://localhost:8000/main_app/api/search/?q=jalan

Expected: JSON Array dengan hasil search
[
    {
        "id": 1,
        "title": "...",
        "location": "...",
        "category": "...",
        "status": "..."
    }
]
```

### Test 6: Detail Report
```
URL: http://localhost:8000/main_app/api/detail/1/

Expected: JSON dengan full detail
{
    "id": 1,
    "title": "...",
    "location": "...",
    "category": "...",
    "description": "...",
    "status": "..."
}
```

---

## 4️⃣ TEST FEATURES DI BROWSER

### Test Live Search:
1. Buka dashboard
2. Scroll ke bawah, cari "🔍 Live Search Laporan"
3. Type di search box (minimal 2 karakter)
4. Lihat hasil tampil di bawah tanpa reload ✅

### Test Charts:
1. Buka dashboard
2. Lihat "📈 Statistik Status Laporan" → Doughnut chart ✅
3. Lihat "📊 Statistik Kategori Laporan" → Bar chart ✅

### Test Detail Modal:
1. Scroll ke bawah, cari "5 Laporan Terbaru"
2. Klik tombol "Detail" pada laporan
3. Modal tampil dengan info lengkap ✅
4. Klik "Tutup" untuk close modal ✅

### Test Responsive Design:
1. Press F12 (Developer Tools)
2. Click device toolbar icon
3. Select "Mobile" atau "Tablet"
4. Lihat apakah layout adjust ✅

---

## 5️⃣ OPEN DEVELOPER TOOLS (Debugging)

### Shortcut:
- **Chrome/Firefox**: Press `F12`
- **Edge**: Press `F12`

### Tabs untuk Check:

**Console Tab:**
- Cek apakah ada error (error akan berwarna merah)
- Cek network calls
- Test command: `console.log('Test')` → harus tampil "Test"

**Network Tab:**
- Refresh page (F5 atau Ctrl+R)
- Lihat semua requests
- Cari `/main_app/api/` requests
- Click request → lihat Response tab
- Response harus JSON format ✅

**Elements Tab:**
- Inspect HTML structure
- Cek apakah canvas element ada
- Cek apakah modal HTML ada

---

## 6️⃣ TROUBLESHOOTING

### Error: Page not found (404)
**Solution**: 
- Check URL spelling
- Verify urls.py updated
- Restart server (Ctrl+C, then `python manage.py runserver`)

### Error: Template not found
**Solution**:
- Check file path: `templates/dashboard.html`
- Check `TEMPLATES['APP_DIRS']` = True di settings.py
- Restart server

### Error: JavaScript console errors
**Solution**:
- Press F12 → Console
- Read error message
- Check [TROUBLESHOOTING_DAN_TIPS.md](TROUBLESHOOTING_DAN_TIPS.md)

### Error: Charts not rendering
**Solution**:
- Check browser console (F12)
- Verify Chart.js CDN loaded (check Network tab)
- Verify API returns data (check `/api/` endpoints)

### Error: Static files 404
**Solution**:
```bash
python manage.py collectstatic
```

---

## 7️⃣ CREATE TEST DATA (Optional)

Jika ingin test dengan data, buat laporan terlebih dahulu:

### Via Django Admin:
```bash
# Buat superuser
python manage.py createsuperuser

# Login ke http://localhost:8000/admin/
# Add Reports manually
```

### Via Django Shell:
```bash
python manage.py shell

# Paste ini:
from main_app.models import Report
Report.objects.create(
    title="Jalan Rusak di Jl. Merdeka",
    location="Jl. Merdeka No.10",
    category="Pothole",
    description="Jalan berlubang besar di depan minimarket",
    status="REPORTED"
)

# Check:
Report.objects.all()

# Exit dengan: exit()
```

---

## 8️⃣ FULL TEST CHECKLIST

Jalankan checklist ini untuk verifikasi:

```
DASHBOARD
├─ [ ] Dashboard page load tanpa error
├─ [ ] 4 statistics cards menampilkan angka
├─ [ ] Doughnut chart render
├─ [ ] Bar chart render
├─ [ ] Latest reported list tampil
├─ [ ] Latest resolved list tampil
└─ [ ] Page responsive (mobile test)

SEARCH FEATURE
├─ [ ] Search input visible
├─ [ ] Type 2+ karakter
├─ [ ] Hasil tampil di bawah
├─ [ ] No page reload
└─ [ ] Clear hasil saat clear search

CHARTS
├─ [ ] Doughnut chart menampilkan semua status
├─ [ ] Bar chart menampilkan kategori
├─ [ ] Hover chart → tooltip tampil
└─ [ ] Chart responsive

MODAL
├─ [ ] Klik "Detail" button
├─ [ ] Modal tampil dengan info
├─ [ ] Tutup button works
└─ [ ] Press Esc untuk close

BROWSER
├─ [ ] F12 Console → no error (red)
├─ [ ] F12 Network → API calls successful (200)
├─ [ ] F12 Elements → HTML structure OK
└─ [ ] Responsive design OK

TOTAL: ___ / 19 checks passed
```

---

## 9️⃣ API TESTING WITH CURL (Advanced)

### Test di Terminal:

```bash
# Test 1
curl http://localhost:8000/main_app/api/status-statistics/

# Test 2
curl http://localhost:8000/main_app/api/category-statistics/

# Test 3
curl http://localhost:8000/main_app/api/latest-reported/

# Test 4
curl http://localhost:8000/main_app/api/latest-resolved/

# Test 5
curl "http://localhost:8000/main_app/api/search/?q=jalan"

# Test 6
curl http://localhost:8000/main_app/api/detail/1/
```

Semua command harus return JSON response ✅

---

## 🔟 STOP SERVER

### Saat Selesai:
```bash
# Press Ctrl+C di terminal
# Server akan berhenti
```

**Output:**
```
Quit the server with CTRL-BREAK.
(Pressed Ctrl+C)
KeyboardInterrupt
```

---

## 📱 MOBILE TESTING

### Desktop Browser Emulation:
1. Press F12
2. Click device toolbar (top left corner)
3. Select device:
   - iPhone 12
   - iPad
   - atau custom resolution
4. Refresh page
5. Test semua fitur di mobile view ✅

---

## ✨ SUCCESS INDICATORS

Anda berhasil jika:

- ✅ Dashboard page accessible
- ✅ Charts render dengan data
- ✅ Search works tanpa reload
- ✅ Modal functionality OK
- ✅ Browser console no errors
- ✅ All API endpoints working
- ✅ Mobile responsive
- ✅ No permission errors

---

## 📊 Performance Check

### Check di F12 → Network Tab:

| Endpoint | Status | Time | Size |
|----------|--------|------|------|
| /dashboard/ | 200 | <500ms | <50KB |
| /api/status-stats | 200 | <100ms | <1KB |
| /api/category-stats | 200 | <100ms | <2KB |
| /api/latest-reported | 200 | <100ms | <5KB |
| /api/latest-resolved | 200 | <100ms | <5KB |
| /api/search | 200 | <200ms | <10KB |
| /api/detail | 200 | <100ms | <2KB |

Target: Response time < 500ms, size < 50KB

---

## 🎯 Before Submit

Final verification:
1. [ ] All features working
2. [ ] No console errors
3. [ ] All API endpoints tested
4. [ ] Code matches PEP8
5. [ ] Documentation complete
6. [ ] Ready to submit! 🎉

---

## 📞 Common Issues While Running

| Issue | Quick Fix |
|-------|-----------|
| Port already in use | `python manage.py runserver 8001` |
| Template error | Restart server |
| Static files missing | `python manage.py collectstatic` |
| Database error | Check if db.sqlite3 exists |
| Import error | Check views.py imports |

---

## 🚀 You're Ready!

Sekarang Anda sudah siap:
- ✅ Menjalankan server
- ✅ Mengakses dashboard
- ✅ Testing semua fitur
- ✅ Debugging dengan DevTools
- ✅ Submit project

**Good luck! 🎉**

---

*Last Updated: April 29, 2026*
*Lab Session 7 - Pemrograman Internet 1*

