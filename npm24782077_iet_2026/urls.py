from django.contrib import admin
from django.urls import path, include
from main_app import views # Pastikan import ini ada

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ubah views.home menjadi views.reports_list agar sinkron dengan views.py
    path('', views.reports_list, name='home'), 
    path('main/', include('main_app.urls')),
]