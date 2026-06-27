from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from main_app.models import Report as MainReport
from reports.models import Report

User = get_user_model()

def make_citizen(username='cov_warga', password='pass1234!'):
    return User.objects.create_user(username=username, email=f'{username}@test.com', password=password, is_staff=False)

def make_admin(username='cov_admin', password='pass1234!'):
    return User.objects.create_user(username=username, email=f'{username}@test.com', password=password, is_staff=True)

def make_main_report(reporter=None, status='REPORTED', title='Test'):
    return MainReport.objects.create(title=title, category='Umum', description='desc', location='Jl. Test', reporter=reporter, status=status)

def make_report(reporter, status=Report.STATUS_DRAFT, title='Test'):
    return Report.objects.create(title=title, description='desc', reporter=reporter, status=status)


class DashboardViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.citizen = make_citizen('dash_warga')

    def test_dashboard_GET(self):
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_POST_valid(self):
        self.client.force_login(self.citizen)
        response = self.client.post('/dashboard/', {'title': 'Jalan Rusak', 'location': 'Jl. Merdeka', 'category': 'Infrastruktur', 'description': 'Berlubang', 'status': 'REPORTED'})
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_POST_missing_title(self):
        self.client.force_login(self.citizen)
        response = self.client.post('/dashboard/', {'title': '', 'location': 'Jl. Merdeka'})
        self.assertIn(response.status_code, [200, 302])

    def test_dashboard_data_json(self):
        response = self.client.get('/dashboard/api/data/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertIn('total', data)

    def test_latest_reported_json(self):
        make_main_report(status='REPORTED', title='Laporan Reported')
        response = self.client.get('/dashboard/api/latest-reported/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_latest_resolved_json(self):
        make_main_report(status='RESOLVED', title='Laporan Resolved')
        response = self.client.get('/dashboard/api/latest-resolved/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)


class MainAppViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.citizen = make_citizen('main_warga')

    def test_reports_list(self):
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_create_report_GET(self):
        response = self.client.get('/main/create/')
        self.assertIn(response.status_code, [200, 302])

    def test_create_report_POST(self):
        self.client.force_login(self.citizen)
        response = self.client.post('/main/create/', {'title': 'Sampah', 'location': 'Jl. Kenanga', 'category': 'Lingkungan', 'description': 'Bau'})
        self.assertIn(response.status_code, [200, 302])

    def test_search_reports(self):
        make_main_report(title='Jalan Berlubang')
        response = self.client.get('/main/search/?q=Jalan')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_search_reports_empty(self):
        response = self.client.get('/main/search/?q=')
        self.assertEqual(response.status_code, 200)

    def test_report_detail_json(self):
        r = make_main_report(title='Detail Test')
        response = self.client.get(f'/main/detail/{r.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Detail Test')

    def test_api_status_statistics(self):
        response = self.client.get('/main/api/status-statistics/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('REPORTED', response.json())

    def test_api_category_statistics(self):
        response = self.client.get('/main/api/category-statistics/')
        self.assertEqual(response.status_code, 200)

    def test_api_latest_reported(self):
        response = self.client.get('/main/api/latest-reported/')
        self.assertEqual(response.status_code, 200)

    def test_api_latest_resolved(self):
        response = self.client.get('/main/api/latest-resolved/')
        self.assertEqual(response.status_code, 200)

    def test_api_search_reports(self):
        response = self.client.get('/main/api/search/?q=test')
        self.assertEqual(response.status_code, 200)

    def test_api_report_detail(self):
        r = make_main_report(title='API Detail')
        response = self.client.get(f'/main/api/detail/{r.id}/')
        self.assertEqual(response.status_code, 200)


class UsermanagementViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = make_citizen('um_warga', 'pass1234!')

    def test_login_GET(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_POST_valid(self):
        response = self.client.post('/login/', {'username': 'um_warga', 'password': 'pass1234!'})
        self.assertIn(response.status_code, [200, 302])

    def test_login_POST_invalid(self):
        response = self.client.post('/login/', {'username': 'um_warga', 'password': 'SALAH'})
        self.assertIn(response.status_code, [200, 302])

    def test_register_GET(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_POST_valid(self):
        response = self.client.post('/register/', {'username': 'newuser99', 'password1': 'StrongPass123!', 'password2': 'StrongPass123!', 'email': 'newuser99@test.com'})
        self.assertIn(response.status_code, [200, 302])

    def test_register_POST_invalid(self):
        response = self.client.post('/register/', {'username': '', 'password1': '123', 'password2': '456'})
        self.assertIn(response.status_code, [200, 302])


class ReportsPermissionExtraTests(APITestCase):
    def setUp(self):
        self.citizen_a = make_citizen('perm_a', 'pass1234!')
        self.citizen_b = make_citizen('perm_b', 'pass1234!')
        self.admin = make_admin('perm_admin', 'pass1234!')
        self.client = APIClient()
        self.url = '/api/reports/'

    def test_unauthenticated_cannot_post(self):
        response = self.client.post(self.url, {'title': 'Test', 'description': 'desc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_cannot_post_report(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(self.url, {'title': 'Admin Buat', 'description': 'desc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_citizen_can_delete_own_draft(self):
        laporan = make_report(self.citizen_a, status=Report.STATUS_DRAFT)
        self.client.force_authenticate(self.citizen_a)
        response = self.client.delete(f'/api/reports/{laporan.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_citizen_cannot_delete_other_draft(self):
        laporan = make_report(self.citizen_b, status=Report.STATUS_DRAFT)
        self.client.force_authenticate(self.citizen_a)
        response = self.client.delete(f'/api/reports/{laporan.id}/')
        self.assertIn(response.status_code, [403, 404])

    def test_admin_cannot_delete_report(self):
        laporan = make_report(self.citizen_a, status=Report.STATUS_REPORTED)
        self.client.force_authenticate(self.admin)
        response = self.client.delete(f'/api/reports/{laporan.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_citizen_can_see_own_draft_detail(self):
        laporan = make_report(self.citizen_a, status=Report.STATUS_DRAFT)
        self.client.force_authenticate(self.citizen_a)
        response = self.client.get(f'/api/reports/{laporan.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_cannot_see_draft(self):
        laporan = make_report(self.citizen_a, status=Report.STATUS_DRAFT)
        self.client.force_authenticate(self.admin)
        response = self.client.get(f'/api/reports/{laporan.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_citizen_list_default_tab(self):
        make_report(self.citizen_a, status=Report.STATUS_REPORTED)
        self.client.force_authenticate(self.citizen_a)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
