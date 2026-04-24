from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Pastikan TIDAK ada namespace di sini jika kamu memanggil {% url 'create' %}
    path('', include('main_app.urls')), 
]