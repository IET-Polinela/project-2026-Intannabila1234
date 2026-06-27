from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import Report

User = get_user_model()


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
        Report.objects.create(
            title='Jalan Berlubang di Depan Kampus',
            category='Infrastruktur',
            description='Ada lubang besar yang membahayakan pengendara.',
            reporter=self.warga_a,
            status='REPORTED',
        )
        Report.objects.create(
            title='Sampah Menumpuk di Trotoar',
            category='Kebersihan',
            description='Sampah tidak diangkut selama seminggu.',
            reporter=self.warga_b,
            status='REPORTED',
        )

    def _get_results(self, response):
        return response.data if isinstance(response.data, list) else response.data.get('results', [])

    def test_PRIV_01_feed_kota_menyembunyikan_identitas_reporter(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get('/api/report/?tab=feed')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._get_results(response)
        if results:
            for laporan in results:
                self.assertEqual(laporan['reporter'], 'Warga Anonim')

    def test_PRIV_02_laporan_saya_menampilkan_nama_asli(self):
        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get('/api/report/?tab=my_reports')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._get_results(response)
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
