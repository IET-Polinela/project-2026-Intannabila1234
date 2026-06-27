from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    """Skenario autentikasi dan akses endpoint terproteksi."""

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

    def test_AUTH_03_akses_endpoint_protected_tanpa_token(self):
        response = self.client.get(reverse('report-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_AUTH_04_akses_endpoint_protected_dengan_token(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('report-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
