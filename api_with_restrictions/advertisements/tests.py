from unittest import TestCase
from rest_framework.test import APIClient


class TestSampleView(TestCase):
    def test_response_ok(self):
        URL = '/api/advertisements/'
        client = APIClient()
        response = client.get(URL)
        self.assertEqual(response.status_code, 200)
