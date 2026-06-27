from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reports.models import Report

User = get_user_model()


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
            status='SELESAI',
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
