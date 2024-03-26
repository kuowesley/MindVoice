import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Test the /api/send-email-notifications/ endpoint
"""
from bciBackend import asgi, wsgi, urls, settings
class UserCredentialTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_send_email_notifications(self):
            response = self.client.get('/api/send-email-notifications/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(json.loads(response.content)['status'], "success")
            self.assertEqual(json.loads(response.content)['message'], "Mail sent successfully")