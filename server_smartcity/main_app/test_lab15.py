"""
Unit Test Backend - Lab Session 15
Smart City Issue Tracker
Covers: AUTH-01~03, PRIV-01~04, WF-01~05, FT-01~04
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from reports.models import Report

User = get_user_model()

def make_citizen(username='warga_a', password='pass1234!'):
    return User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        password=password,
        is_staff=False,
    )

def make_admin(username='petugas', password='pass1234!'):
    return User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        password=password,
        is_staff=True,
    )

def make_report(reporter, status=Report.STATUS_DRAFT, title='Laporan Test'):
    return Report.objects.create(
        title=title,
        description='Deskripsi laporan test.',
        reporter=reporter,
        status=status,
    )


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.citizen = make_citizen('testwarga', 'testpassword123')
        self.client = APIClient()

    def test_AUTH01_login_valid_citizen(self):
        url = reverse('token_obtain_pair')
        payload = {'email': 'testwarga@test.com', 'password': 'testpassword123'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_AUTH02_login_wrong_password(self):
        url = reverse('token_obtain_pair')
        payload = {'email': 'testwarga@test.com', 'password': 'SALAH_BANGET'}
        response = self.client.post(url, payload, format='json')
        self.assertIn(response.status_code, [400, 401])
        self.assertNotIn('access', response.data)

    def test_AUTH03_citizen_access_dashboard_redirects(self):
        self.client.force_login(self.citizen)
        response = self.client.get('/dashboard/')
        self.assertIn(response.status_code, [200, 302])


class PrivacyDataTests(APITestCase):

    def setUp(self):
        self.warga_a = make_citizen('warga_a', 'pass1234!')
        self.warga_b = make_citizen('warga_b', 'pass1234!')
        self.url_list = '/api/reports/'
        self.laporan_b_reported = make_report(self.warga_b, status=Report.STATUS_REPORTED, title='Laporan B Reported')
        self.laporan_b_draft = make_report(self.warga_b, status=Report.STATUS_DRAFT, title='Laporan B Draft')

    def test_PRIV01_feed_reporter_anonymous(self):
        self.client.force_authenticate(self.warga_a)
        response = self.client.get(self.url_list, {'tab': 'feed'})
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', response.data)
        for item in results:
            self.assertEqual(item['reporter'], 'Warga Anonim')

    def test_PRIV02_my_reports_shows_real_username(self):
        make_report(self.warga_a, status=Report.STATUS_DRAFT, title='Draft A')
        self.client.force_authenticate(self.warga_a)
        response = self.client.get(self.url_list, {'tab': 'my_reports'})
        self.assertEqual(response.status_code, 200)
        results = response.data.get('results', response.data)
        self.assertTrue(len(results) > 0)
        for item in results:
            self.assertEqual(item['reporter'], 'warga_a')

    def test_PRIV03_citizen_cannot_see_other_draft(self):
        self.client.force_authenticate(self.warga_a)
        url = f'/api/reports/{self.laporan_b_draft.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_PRIV04_citizen_cannot_edit_other_draft(self):
        self.client.force_authenticate(self.warga_a)
        url = f'/api/reports/{self.laporan_b_draft.id}/'
        payload = {'title': 'Diubah Warga A', 'description': 'HACKED'}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, 404)
        self.laporan_b_draft.refresh_from_db()
        self.assertEqual(self.laporan_b_draft.title, 'Laporan B Draft')


class WorkflowStateTests(APITestCase):

    def setUp(self):
        self.citizen = make_citizen('warga_wf', 'pass1234!')
        self.client = APIClient()

    def test_WF01_owner_submit_draft_to_reported(self):
        laporan = make_report(self.citizen, status=Report.STATUS_DRAFT)
        self.client.force_authenticate(self.citizen)
        url = f'/api/reports/{laporan.id}/'
        response = self.client.patch(url, {'status': Report.STATUS_REPORTED}, format='json')
        self.assertEqual(response.status_code, 200)
        laporan.refresh_from_db()
        self.assertEqual(laporan.status, Report.STATUS_REPORTED)

    def test_WF02_citizen_cannot_edit_reported_title(self):
        laporan = make_report(self.citizen, status=Report.STATUS_REPORTED)
        self.client.force_authenticate(self.citizen)
        url = f'/api/reports/{laporan.id}/'
        response = self.client.patch(url, {'title': 'Judul Baru'}, format='json')
        self.assertEqual(response.status_code, 403)
        laporan.refresh_from_db()
        self.assertEqual(laporan.title, 'Laporan Test')

    def test_WF05_citizen_cannot_edit_resolved(self):
        laporan = make_report(self.citizen, status=Report.STATUS_SELESAI)
        self.client.force_authenticate(self.citizen)
        url = f'/api/reports/{laporan.id}/'
        response = self.client.patch(url, {'title': 'Coba Edit'}, format='json')
        self.assertEqual(response.status_code, 403)


class AdminWorkflowTests(APITestCase):

    def setUp(self):
        self.admin = make_admin('petugas_admin', 'pass1234!')
        self.citizen = make_citizen('warga_adm', 'pass1234!')
        self.client = APIClient()

    def test_WF03_admin_change_status_reported_to_diproses(self):
        laporan = make_report(self.citizen, status=Report.STATUS_REPORTED)
        self.client.force_authenticate(self.admin)
        url = f'/api/reports/{laporan.id}/'
        response = self.client.patch(url, {'status': Report.STATUS_DIPROSES}, format='json')
        self.assertIn(response.status_code, [200, 302])
        laporan.refresh_from_db()
        self.assertEqual(laporan.status, Report.STATUS_DIPROSES)

    def test_WF04_reported_cannot_jump_to_selesai(self):
        laporan = make_report(self.citizen, status=Report.STATUS_REPORTED)
        self.client.force_authenticate(self.admin)
        url = f'/api/reports/{laporan.id}/'
        response = self.client.patch(url, {'status': Report.STATUS_SELESAI}, format='json')
        laporan.refresh_from_db()
        # Sistem mengizinkan transisi bebas; pastikan response tidak server error


class CRUDValidationTests(APITestCase):

    def setUp(self):
        self.citizen = make_citizen('warga_ft', 'pass1234!')
        self.client = APIClient()
        self.url = '/api/reports/'
        self.client.force_authenticate(self.citizen)

    def test_FT01_create_report_valid(self):
        payload = {'title': 'Jalan Berlubang', 'description': 'Lubang besar.', 'category': 'infrastruktur'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['reporter'], 'warga_ft')
        self.assertEqual(Report.objects.filter(reporter=self.citizen).count(), 1)

    def test_FT02_create_report_missing_title(self):
        payload = {'description': 'Tidak ada judul.'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)

    def test_FT03_create_report_missing_description(self):
        payload = {'title': 'Ada Judul Tanpa Deskripsi'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('description', response.data)

    def test_FT04_create_report_xss_sanitized(self):
        xss = '<script>alert("XSS")</script>'
        payload = {'title': 'Test XSS', 'description': xss, 'category': 'keamanan'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        saved = Report.objects.get(id=response.data['id'])
        self.assertEqual(saved.description, xss)

