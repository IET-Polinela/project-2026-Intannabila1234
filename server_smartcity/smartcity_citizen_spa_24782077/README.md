# Smart City Citizen - Vanilla JS SPA

Project sederhana Single Page Application (SPA) untuk tugas Lab Session 11 (Routing & Authentication) menggunakan Vanilla JavaScript dan Bootstrap 5.

Run locally:

1. Buka terminal di folder project root (satu level di atas `smartcity_citizen_spa_npm`).
2. Jalankan server static sederhana:

```bash
python -m http.server 5500
```

3. Buka browser ke:

http://127.0.0.1:5500/

Catatan:
- Endpoint token login di `auth.js` menggunakan `http://127.0.0.1:8000/api/token/`. Pastikan backend Django REST API berjalan dan mengizinkan CORS.
- Files utama berada di `smartcity_citizen_spa_npm/js/`.

Quick testing helper:

- The SPA will populate demo credentials into `localStorage` automatically on first load for convenience.
- Demo email: `citizen_lab10@gmail.com`
	- Demo password: `CitizenPass123`

When you open the login page, the form inputs will be prefilled with these demo credentials.

