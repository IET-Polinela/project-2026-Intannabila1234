from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenRefreshView

from dashboard_24782077.views import dashboard
from usermanagement_24782077.views import register, login_view
from usermanagement.api_views import RegisterView, EmailTokenObtainPairView
from main_app import views as main_views

# --- TAMBAHAN IMPORT BARU LAB 14 (MULAI DI SINI) ---
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer
# --- AKHIR IMPORT BARU LAB 14 ---

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Root -> langsung render dashboard baru
    path('', dashboard, name='home'),

    # Template views
    path('reports/', RedirectView.as_view(url='/dashboard/', permanent=False), name='reports'),
    path('main/',   include('main_app.urls', namespace='main_app')),
    path('dashboard/', include('dashboard_24782077.urls', namespace='dashboard')),

    # Auth (session-based)
    path('login/',    login_view,              name='login'),
    path('logout/',   LogoutView.as_view(),    name='logout'),
    path('register/', register,                name='register'),

    # JWT endpoints
    path('api/token/',         EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),         name='token_refresh'),

    # REST API routers
    path('api/',              include('main_app.api_urls')),
    path('api/reports/',      include('reports.urls')),
    path('api/usermanagement/', include('usermanagement.urls')),

    # Short alias untuk register
    path('api/register/', RegisterView.as_view(), name='api-register-alias'),

    # --- TAMBAHAN PATH ENDPOINT BARU LAB 14 (MULAI DI SINI) ---
    # 1. Endpoint untuk meng-generate file skema mentah (JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Endpoint Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Endpoint Scalar UI
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
    # --- AKHIR PATH ENDPOINT BARU LAB 14 ---
]