"""
URL configuration for the dashboard app.
"""

from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.dashboard, name='add_report'),
    path('api/data/', views.dashboard_data, name='api_data'),
    path('api/latest-reported/', views.latest_reported, name='api_latest_reported'),
    path('api/latest-resolved/', views.latest_resolved, name='api_latest_resolved'),
]
