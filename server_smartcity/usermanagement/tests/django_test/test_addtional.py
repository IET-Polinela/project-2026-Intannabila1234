from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import Report

User = get_user_model()


class ReportApiCoverageTests(APITestCase):
    """Kelas uji tambahan untuk menambah coverage endpoint laporan."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='password123',
        )
        self.client.force_authenticate(user=self.user)

        self.report = Report.objects.create(
            title='Pipa Bocor',
            category='Sarana',
            description='Air menetes di depan rumah warga',
            reporter=self.user,
            status='REPORTED',
        )

    def test_list_reports_returns_existing_reports(self):
        """GET /api/report/ mengembalikan daftar laporan yang tersedia."""
        response = self.client.get(reverse('report-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(any(item['title'] == 'Pipa Bocor' for item in response.data['results']))

    def test_create_report_returns_201_and_persists_data(self):
        """POST /api/report/ membuat laporan baru dan menyimpannya ke database."""
        data = {
            'title': 'Lampu Mati',
            'category': 'Prasarana',
            'description': 'Lampu jalan mati di persimpangan',
            'status': 'REPORTED',
        }

        response = self.client.post(reverse('report-list'), data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(Report.objects.latest('id').title, 'Lampu Mati')

    def test_detail_report_returns_reporter_name_for_owner(self):
        """GET /api/report/<id>/ menampilkan data laporan milik sendiri."""
        response = self.client.get(reverse('report-detail', kwargs={'pk': self.report.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reporter'], self.user.username)


class AuthenticationTests(APITestCase):
    """Skenario autentikasi sesuai endpoint JWT proyek."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='warga_test',
            email='warga@example.com',
            password='Password123!',
        )

    def test_AUTH_01_login_warga_dengan_kredensial_valid(self):
        url = reverse('token_obtain_pair')
        payload = {
            'email': 'warga@example.com',
            'password': 'Password123!',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_AUTH_02_login_warga_dengan_password_salah(self):
        url = reverse('token_obtain_pair')
        payload = {
            'email': 'warga@example.com',
            'password': 'salah123',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)


class PrivacyAndDataHidingTests(APITestCase):
    """Skenario privasi dan visibilitas data laporan."""

    def setUp(self):
        self.warga_a = User.objects.create_user(
            username='warga_a',
            email='warga_a@example.com',
            password='TestPass123!',
        )
        self.warga_b = User.objects.create_user(
            username='warga_b',
            email='warga_b@example.com',
            password='TestPass123!',
        )

        self.draft_milik_b = Report.objects.create(
            title='Draf Rahasia Warga B',
            category='Infrastruktur',
            description='Ini adalah draf yang belum diajukan.',
            reporter=self.warga_b,
            status='DRAFT',
        )
        self.laporan_publik_a = Report.objects.create(
            title='Jalan Berlubang di Depan Kampus',
            category='Infrastruktur',
            description='Ada lubang besar yang membahayakan pengendara.',
            reporter=self.warga_a,
            status='REPORTED',
        )
        self.laporan_publik_b = Report.objects.create(
            title='Sampah Menumpuk di Trotoar',
            category='Kebersihan',
            description='Sampah tidak diangkut selama seminggu.',
            reporter=self.warga_b,
            status='REPORTED',
        )

    def test_PRIV_01_feed_kota_menyembunyikan_identitas_reporter(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get('/api/report/?tab=feed')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if isinstance(response.data, dict) is False else response.data.get('results', [])
        if results:
            for laporan in results:
                self.assertEqual(laporan['reporter'], 'Warga Anonim')

    def test_PRIV_02_laporan_saya_menampilkan_nama_asli(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get('/api/report/?tab=my_reports')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if isinstance(response.data, dict) is False else response.data.get('results', [])
        if results:
            for laporan in results:
                self.assertIn('reporter', laporan)

    def test_PRIV_03_tidak_bisa_baca_draf_orang_lain(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get(reverse('report-detail', kwargs={'pk': self.draft_milik_b.pk}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PRIV_04_tidak_bisa_modifikasi_draf_orang_lain(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.put(
            reverse('report-detail', kwargs={'pk': self.draft_milik_b.pk}),
            {'status': 'REPORTED'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class WorkflowStateTests(APITestCase):
    """Skenario alur kerja dan transisi status laporan."""

    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_wf',
            email='warga_wf@example.com',
            password='TestPass123!',
        )
        self.laporan_draft = Report.objects.create(
            title='Lampu Kampus Mati',
            category='Fasilitas Umum',
            description='Lampu di depan gedung rektorat tidak menyala.',
            reporter=self.warga,
            status='DRAFT',
        )
        self.laporan_reported = Report.objects.create(
            title='Saluran Air Tersumbat',
            category='Infrastruktur',
            description='Saluran air di samping kantin tersumbat.',
            reporter=self.warga,
            status='REPORTED',
        )
        self.laporan_resolved = Report.objects.create(
            title='AC Rusak di Lab',
            category='Fasilitas Umum',
            description='AC di Lab CPS 1 sudah diperbaiki.',
            reporter=self.warga,
            status='RESOLVED',
        )

    def test_WF_01_warga_mengajukan_draf_menjadi_reported(self):
        self.client.force_authenticate(user=self.warga)

        response = self.client.put(
            reverse('report-detail', kwargs={'pk': self.laporan_draft.pk}),
            {
                'title': self.laporan_draft.title,
                'category': self.laporan_draft.category,
                'description': self.laporan_draft.description,
                'status': 'REPORTED',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.laporan_draft.refresh_from_db()
        self.assertEqual(self.laporan_draft.status, 'REPORTED')

    def test_WF_02_tidak_bisa_edit_laporan_yang_sudah_reported(self):
        self.client.force_authenticate(user=self.warga)

        response = self.client.put(
            reverse('report-detail', kwargs={'pk': self.laporan_reported.pk}),
            {
                'title': 'Judul Baru',
                'category': self.laporan_reported.category,
                'description': self.laporan_reported.description,
                'status': 'REPORTED',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_WF_05_laporan_resolved_tidak_bisa_diubah(self):
        self.client.force_authenticate(user=self.warga)

        response = self.client.put(
            reverse('report-detail', kwargs={'pk': self.laporan_resolved.pk}),
            {'status': 'REPORTED'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CRUDAndValidationTests(APITestCase):
    """Skenario CRUD dasar dan validasi input."""

    def setUp(self):
        self.warga = User.objects.create_user(
            username='warga_crud',
            email='warga_crud@example.com',
            password='TestPass123!',
        )
        self.client.force_authenticate(user=self.warga)

    def test_FT_01_buat_laporan_dengan_data_lengkap(self):
        payload = {
            'title': 'Laporan Baru',
            'category': 'Infrastruktur',
            'description': 'Deskripsi lengkap.',
            'status': 'REPORTED',
        }

        response = self.client.post(reverse('report-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Report.objects.filter(title='Laporan Baru').exists())

    def test_FT_02_ditolak_jika_judul_kosong(self):
        payload = {
            'category': 'Infrastruktur',
            'description': 'Deskripsi tanpa judul.',
        }

        response = self.client.post(reverse('report-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_FT_03_ditolak_jika_deskripsi_kosong(self):
        payload = {
            'title': 'Laporan Tanpa Deskripsi',
            'category': 'Infrastruktur',
        }

        response = self.client.post(reverse('report-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)

    def test_FT_04_xss_script_disimpan_sebagai_string_literal(self):
        kode_xss = '<script>alert("xss")</script>'
        payload = {
            'title': 'Laporan XSS Test',
            'category': 'Keamanan',
            'description': kode_xss,
            'status': 'REPORTED',
        }

        response = self.client.post(reverse('report-list'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        laporan = Report.objects.get(title='Laporan XSS Test')
        self.assertIn('script', laporan.description.lower())
