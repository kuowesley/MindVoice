from django.test import TestCase, Client
from config import asgi, wsgi, urls, settings
from django.contrib.auth.models import User
from analyzeapp.models import LabelUsage, UserFeedback

"""
Test saving label usage data
"""


class SaveUsageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_save_usage(self):
        # get the first user
        user = User.objects.first()
        self.assertIsNotNone(user, "No user found in the database")
        usage = LabelUsage(user=user, label=3)
        usage.save()
        self.assertIsNotNone(usage.id, "Failed to save usage data")
        
    def test_log_usage(self):
        user = User.objects.first()
        self.assertIsNotNone(user, "No user found in the database")
        self.client.force_login(user)
        response = self.client.post('/api/log-usage/', {'label': 3}, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200, "Failed to log usage data")
        self.assertEqual(response.json()['status'], 'success', "Failed to log usage data")
        
    def test_save_feedback(self):
        user = User.objects.first()
        self.assertIsNotNone(user, "No user found in the database")
        self.client.force_login(user)
        response = self.client.post('/api/create-user-feedback/', {'feedback': "This is a test feedback"}, content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, 200, "Failed to save feedback")
        self.assertEqual(response.json()['status'], 'success', "Failed to save feedback")
        print(UserFeedback.objects.all())