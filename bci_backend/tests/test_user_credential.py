import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Test the /api/health/ endpoint
"""
from bciBackend import asgi, wsgi, urls, settings
class UserCredentialTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_success(self):
        response = self.client.post('/api/login/', json.dumps({
            "user": "test_user1",
            "password": "Example1"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "login success")
        
    def test_login_fail_1(self):
        response = self.client.post('/api/login/', json.dumps({
            "user": "wrong_user",
            "password": "password"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "login failed")
        
    def test_login_fail_2(self):
        response = self.client.post('/api/login/', json.dumps({
            "user": "test_user1",
            "password": "wrong_password"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "login failed")
    
    def test_register_failed(self):
        response = self.client.post('/api/register/', json.dumps({
            "user": "test_user1",
            "password": "Example1"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "Username already exists")
