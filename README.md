## 👩‍💻 About Me

- 🌷 Nama: **Intan Nabila**
- 🎓 NPM: **24782077**

---

## 🧪 Postman DELETE Request untuk Report API

Gunakan method `DELETE` dengan URL:

```text
http://127.0.0.1:8000/api/report/<id>/
```

Headers:
- `Authorization: Bearer <access_token>`
- `Content-Type: application/json`

Body: kosong

### Hasil yang diharapkan
- `204 No Content` → penghapusan berhasil
- `403 Forbidden` → tidak memiliki izin delete
- `401 Unauthorized` → token tidak valid atau tidak dikirim

### Catatan akses
- Hanya `Citizen` yang boleh menghapus report miliknya
- `Admin` tidak boleh menghapus report
