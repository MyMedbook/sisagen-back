# authentication/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import requests

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.token_url = reverse('token_obtain')
        self.test_credentials = {
            'username': 'iskender.wolfer@gmail.com',
            'password': '7879Hi@@@'
        }

    def test_obtain_token(self):
        response = self.client.post(self.token_url, self.test_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('token_type', response.data)
        self.assertIn('expires_in', response.data)
        self.assertIn('refresh_token', response.data)