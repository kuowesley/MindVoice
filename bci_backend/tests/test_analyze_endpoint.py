import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Test the /api/analyze/ endpoint
"""
class AnalyzeDataTestCase(TestCase):
    from bciBackend import asgi, wsgi, urls, settings
    def setUp(self):
        self.label_mapping = {
            'hello.json': 0,
            'help_me.json': 1,
            'stop.json': 2,
            'thank_you.json': 3,
            'yes.json': 4
        }
        self.data = {
            'data': [],
            'time': '2024-03-01T12:00:00',
            'UserName': 'test_user'
        }
        self.client = Client()

    def load_request_data(self, file_name):
        with open(os.path.join(settings.BASE_DIR, 'tests', file_name)) as f:
            self.data['data'] = json.load(f).get('data')
            print(self.data['data'])
    
    def assert_response_valid(self, response_data):
        self.assertIn('label', response_data)
        self.assertIn('time', response_data)
        self.assertIn('UserName', response_data)
        self.assertEqual(response_data['time'], self.data['time'])
        self.assertEqual(response_data['UserName'], self.data['UserName'])

    def test_analyze_data_endpoint(self):
        for file_name, label in self.label_mapping.items():
            self.load_request_data(file_name)
            response = self.client.post('/api/analyze/', json.dumps(self.data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.content)
            self.assert_response_valid(response_data)
            self.assertEqual(response_data['label'], label)
    
    def test_analyze_data_endpoint_invalid(self):
        response = self.client.post('/api/analyze/', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'error': 'No data provided'})

    def test_analyze_data_endpoint_invalid_2(self):
        invalidJson = '{"test": "test'
        response = self.client.post('/api/analyze/', invalidJson, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data, {'error':'Invalid JSON'})

