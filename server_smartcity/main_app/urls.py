from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Dashboard & Statistik
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # API Endpoints untuk Dashboard
    path('api/status-statistics/', views.api_status_statistics, name='api_status_stats'),
    path('api/category-statistics/', views.api_category_statistics, name='api_category_stats'),
    path('api/latest-reported/', views.api_latest_reported, name='api_latest_reported'),
    path('api/latest-resolved/', views.api_latest_resolved, name='api_latest_resolved'),
    path('api/search/', views.api_search_reports, name='api_search'),
    path('api/detail/<int:report_id>/', views.api_report_detail, name='api_detail'),
    
    # Laporan & CRUD Operations
    path('', views.reports_list, name='reports_list'),
    path('create/', views.create_report, name='create'),
    path('verify/<int:report_id>/', views.verify_report, name='verify'),
    path('progress/<int:report_id>/', views.progress_report, name='progress'),
    path('resolve/<int:report_id>/', views.resolve_report, name='resolve'),
    path('update/<int:report_id>/', views.update_report, name='update'),
    path('delete/<int:report_id>/', views.delete_report, name='delete'),
    # API Endpoints untuk Live Search & Modal Detail
    path('search/', views.search_reports, name='search'),           # /main/search/?q=...
    path('detail/<int:report_id>/', views.report_detail, name='detail'),  # /main/detail/123/

]