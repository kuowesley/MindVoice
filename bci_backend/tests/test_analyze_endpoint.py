import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Testing the analyze endpoint
"""
from bciBackend import asgi, wsgi, urls, settings
class AnalyzeDataTestCase(TestCase):
    def setUp(self):
        self.label_mapping = {
            'hello.json': 0,
            'help_me.json': 1,
            'stop.json': 2,
            'thank_you.json': 3,
            'yes.json': 4
        }
        self.client = Client()

    def load_request_data(self, file_name):
        with open(os.path.join(settings.BASE_DIR, 'tests', file_name)) as f:
            data = {
                'data': json.load(f).get('data'),
                'time': '2024-03-01T12:00:00',
                'UserName': 'test_user'
            }
        return data
    
    def assert_response_valid(self, response_data, data):
        self.assertIn('label', response_data)
        self.assertIn('time', response_data)
        self.assertIn('UserName', response_data)
        self.assertEqual(response_data['time'], data['time'])
        self.assertEqual(response_data['UserName'], data['UserName'])

    def test_analyze_data_endpoint(self):
        for file_name, label in self.label_mapping.items():
            data = self.load_request_data(file_name)
            response = self.client.post('/api/analyze/', json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.content)
            self.assert_response_valid(response_data, data)
            self.assertEqual(response_data['label'], label)
