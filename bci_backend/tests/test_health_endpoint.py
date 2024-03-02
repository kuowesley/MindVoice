import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Testing the analyze endpoint
"""
from bciBackend import asgi, wsgi, urls, settings
class HealthCheckTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"status": "ok"}')
