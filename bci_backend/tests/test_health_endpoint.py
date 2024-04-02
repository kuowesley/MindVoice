from django.test import TestCase, Client

"""
Test the /api/health/ endpoint
"""


class HealthCheckTestCase(TestCase):
    from config import asgi, wsgi, urls, settings

    def setUp(self):
        self.client = Client()

    def test_health_endpoint(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"status": "ok"}')
