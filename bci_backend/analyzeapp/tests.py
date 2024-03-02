from django.test import TestCase, Client
import json

class AnalyzeDataTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_analyze_data_endpoint(self):
        # prepare the data to be sent in the request
        data = {
            'data': [], # still needs to be configured, 
            'time': '2024-03-01T12:00:00',
            'UserName': 'test_user'
        }
        # send a POST request to the /analyze endpoint in "api.py"
        response = self.client.post('/analyze', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)

        #cCheck if the response contains the expected keys
        self.assertIn('label', response_data)
        self.assertIn('time', response_data)
        self.assertIn('UserName', response_data)

        # check if the label is a string
        self.assertIsInstance(response_data['label'], str)

        # check if the time and UserName match the input data
        self.assertEqual(response_data['time'], data['time'])
        self.assertEqual(response_data['UserName'], data['UserName'])
