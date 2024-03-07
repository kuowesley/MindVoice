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

    def load_request_data(self, file_name, append=""):
        with open(os.path.join(settings.BASE_DIR, 'tests', append, file_name)) as f:
            self.data['data'] = json.load(f).get('data')
            #print(self.data['data'])
    
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
        
    def test_analyze_test_accuracy(self):
        for label in [0, 1, 2, 3, 4]:
            correct = 0.0
            total = 0.0
            for file_name in os.listdir(os.path.join(settings.BASE_DIR, 'tests/test_data')):
                if file_name.startswith(str(label)):
                    self.load_request_data(file_name, "test_data")
                    response = self.client.post('/api/analyze/', json.dumps(self.data), content_type='application/json')
                    response_data = json.loads(response.content)
                    if response_data['label'] == label: correct += 1
                    total += 1
            self.assertGreater((correct / total), 0.68, "Accuracy less than 68% for " + str(label) + " - " + str((correct / total)))
            
    def test_analyze_test_recall_precision(self):
        FP = TP = FN = TN = 0.0
        for label in [0, 1, 2, 3, 4]:
            for file_name in os.listdir(os.path.join(settings.BASE_DIR, 'tests/test_data')):
                if file_name.startswith(str(label)):
                    self.load_request_data(file_name, "test_data")
                    response = self.client.post('/api/analyze/', json.dumps(self.data), content_type='application/json')
                    response_data = json.loads(response.content)
                    TP += (response_data['label'] == label and label in (0, 3, 4)) # 'Positive' feeling labels
                    TN += (response_data['label'] == label and label in (1, 2)) # 'Negative' feeling labels
                    FP += (response_data['label'] != label and label in (0, 3, 4))
                    FN += (response_data['label'] != label and label in (1, 2))
        
        # Recall: TP / (TP + FN)
        recall = TP / (TP + FN) if TP + FN != 0 else 0 # prevent div 0
        
        # Precision: TP / (TP + FP)
        precision = TP / (TP + FP) if TP + FP != 0 else 0 # prevent div 0
        
        self.assertGreater(recall, 0.7, "Recall less than 70%! " + str(recall))
        self.assertGreater(precision, 0.7, "Precision less than 70%! " + str(precision))