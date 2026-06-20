import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_app.settings')
import django

django.setup()

from django.test import Client

c = Client()
urls = ['/dashboard/', '/dashboard/add/', '/login/', '/register/']
for u in urls:
    r = c.get(u)
    html = r.content.decode('utf-8', 'ignore')
    title = html.split('<title>')[1].split('</title>')[0] if '<title>' in html else 'NO_TITLE'
    print(f'URL={u} STATUS={r.status_code} TITLE={title}')
    print('HAS_EMAIL_FIELD=', 'name="email"' in html)
    print('HAS_ADD_MARKER=', 'Buat Laporan Baru' in html or 'Kirim Laporan Resmi' in html)
    print('HAS_LOGIN_MARKER=', 'SmartCity_Apuh - Login' in html or 'Masuk' in html)
    print('HAS_REGISTER_MARKER=', 'SmartCity_Apuh - Register' in html or 'Buat akun SmartCity_Apuh' in html)
    print('-----')

post = c.post('/dashboard/add/', {
    'title': 'Tes final',
    'category': 'Infrastruktur',
    'description': 'cek submit',
    'location': 'Jl. Test',
    'status': 'REPORTED'
})
print('ADD_POST_STATUS=', post.status_code)
print('ADD_REDIRECT=', post.headers.get('Location'))
