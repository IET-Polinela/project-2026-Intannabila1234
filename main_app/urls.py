from django.urls import path
from . import views

urlpatterns = [
    # Path untuk fitur laporan
    path('reports/', views.reports_list, name='reports_list'),
    path('create/', views.create_report, name='create'),
    path('update/<int:id>/', views.update_report, name='update'),
    path('delete/<int:id>/', views.delete_report, name='delete'),

    # Path untuk workflow status
    path('verify/<int:id>/', views.verify_report, name='verify'),
    path('progress/<int:id>/', views.progress_report, name='progress'),
    path('resolve/<int:id>/', views.resolve_report, name='resolve'),
]