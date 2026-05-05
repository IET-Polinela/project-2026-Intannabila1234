"""
URL Configuration untuk Dashboard App
Dashboard_24782077 urls.py
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard main view (TemplateView)
    # URL: /dashboard/
    path('', views.DashboardView.as_view(), name='index'),
    
    # API Endpoints untuk Chart.js
    # URL: /dashboard/api/data/
    path('api/data/', views.dashboard_data, name='api_data'),
    
    # URL: /dashboard/api/latest-reported/
    path('api/latest-reported/', views.latest_reported, name='api_latest_reported'),
    
    # URL: /dashboard/api/latest-resolved/
    path('api/latest-resolved/', views.latest_resolved, name='api_latest_resolved'),
]
