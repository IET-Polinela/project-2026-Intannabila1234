from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import Report

User = get_user_model()


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
