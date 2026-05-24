from django.contrib import admin
from django.urls import path, include
from main_app import views  # Pastikan import ini ada
from django.contrib.auth.views import LoginView, LogoutView
from usermanagement_24782077.views import register, login_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from usermanagement.api_views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ubah views.home menjadi views.reports_list agar sinkron dengan views.py
    path('', views.reports_list, name='home'),
    path('reports/', views.reports_list, name='reports'),
    path('main/', include('main_app.urls', namespace='main_app')),
    # Dashboard URLs - NEW
    path('dashboard/', include('dashboard_24782077.urls', namespace='dashboard')),
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('api/', include('main_app.api_urls')),
    # JWT token endpoints (Lab 10)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API routers for reports and usermanagement
    path('api/reports/', include('reports.urls')),
    path('api/usermanagement/', include('usermanagement.urls')),
    # Short alias for register endpoint
    path('api/register/', RegisterView.as_view(), name='api-register-alias'),
]