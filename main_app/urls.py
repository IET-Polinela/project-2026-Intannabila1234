from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.reports_list, name='reports_list'),
    path('create/', views.create_report, name='create'),
    path('verify/<int:report_id>/', views.verify_report, name='verify'),
    path('progress/<int:report_id>/', views.progress_report, name='progress'),
    path('resolve/<int:report_id>/', views.resolve_report, name='resolve'),
    path('update/<int:report_id>/', views.update_report, name='update'),
    path('delete/<int:report_id>/', views.delete_report, name='delete'),
]