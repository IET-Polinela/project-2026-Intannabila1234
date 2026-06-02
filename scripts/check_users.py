from pathlib import Path
import sys, os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npm24782077_iet_2026.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def check(username, password):
    try:
        u = User.objects.get(username=username)
        print(username, 'exists, is_active=', u.is_active)
        print('check_password ->', u.check_password(password))
    except User.DoesNotExist:
        print(username, 'DOES NOT EXIST')

if __name__ == '__main__':
    check('admin_lab10', 'AdminPass123')
    check('citizenlab10', 'CitizenPass123')
