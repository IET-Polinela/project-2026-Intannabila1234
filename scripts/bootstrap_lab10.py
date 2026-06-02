import os
import sys
from pathlib import Path
import django
from django.conf import settings

# Ensure project root is on sys.path so the project package can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npm24782077_iet_2026.settings')
django.setup()

from django.contrib.auth import get_user_model
from reports.models import Report
from rest_framework_simplejwt.tokens import RefreshToken
import argparse

User = get_user_model()

def create_users_and_report(show_tokens=False):
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

    # Print usernames and passwords only. Tokens are sensitive and hidden by default.
    print('ADMIN:', admin_username, 'password=', admin_password)
    print('\nCITIZEN:', citizen_username, 'password=', citizen_password)

    if show_tokens:
        # Print tokens only when explicitly requested
        admin_tokens = RefreshToken.for_user(admin)
        citizen_tokens = RefreshToken.for_user(citizen)
        print('\n[Tokens - developer flag --show-tokens enabled]')
        print('ADMIN access token (short):', str(admin_tokens.access_token))
        print('ADMIN refresh token:', str(admin_tokens))
        print('\nCITIZEN access token (short):', str(citizen_tokens.access_token))
        print('CITIZEN refresh token:', str(citizen_tokens))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bootstrap lab users and sample report')
    parser.add_argument('--show-tokens', action='store_true', help='Print JWT tokens to stdout (for debugging only)')
    args = parser.parse_args()
    create_users_and_report(show_tokens=args.show_tokens)
