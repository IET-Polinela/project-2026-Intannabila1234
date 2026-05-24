import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npm24782077_iet_2026.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import Report
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def create_users_and_report():
    admin_username = 'admin_lab10'
    admin_email = 'admin_lab10@example.com'
    admin_password = 'AdminPass123'

    citizen_username = 'citizenlab10'
    citizen_email = 'citizen_lab10@example.com'
    citizen_password = 'CitizenPass123'

    admin, created = User.objects.get_or_create(username=admin_username, defaults={'email': admin_email, 'is_staff': True, 'is_superuser': True})
    if created:
        admin.set_password(admin_password)
        admin.save()

    citizen, created = User.objects.get_or_create(username=citizen_username, defaults={'email': citizen_email})
    if created:
        citizen.set_password(citizen_password)
        citizen.save()

    # Create a sample DRAFT report for citizen if none exists
    if not Report.objects.filter(reporter=citizen).exists():
        Report.objects.create(title='Contoh Laporan Jalan Rusak', description='Bagian jalan berlubang', reporter=citizen)

    # Print tokens for manual testing
    admin_tokens = RefreshToken.for_user(admin)
    citizen_tokens = RefreshToken.for_user(citizen)

    print('ADMIN:', admin_username, 'password=', admin_password)
    print('ADMIN access token (short):', str(admin_tokens.access_token))
    print('ADMIN refresh token:', str(admin_tokens))
    print('\nCITIZEN:', citizen_username, 'password=', citizen_password)
    print('CITIZEN access token (short):', str(citizen_tokens.access_token))
    print('CITIZEN refresh token:', str(citizen_tokens))

if __name__ == '__main__':
    create_users_and_report()
