import os
from django.conf import settings
from django.test import TestCase, Client
import json

"""
Test the /api/login/ and /api/register/ endpoint
"""
from bciBackend import asgi, wsgi, urls, settings
class UserCredentialTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        

    def test_login_success(self):
        response = self.client.post('/api/login/', json.dumps({
            "user": "test_user6",
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
            "user": "test_user6",
            "password": "wrong_password"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "login failed")
    
    def test_register_failed(self):
        response = self.client.post('/api/register/', json.dumps({
            "user": "test_user6",
            "password": "Example1"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "Registration failed")
    
    def test_delete_user(self):
        response = self.client.delete('/api/delete/', json.dumps({
            "user": "test_user6",
            "password": "Example1"
        }), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "Successfully deleted the user")
    
    def test_delete_invalid(self):
        response = self.client.delete('/api/delete/', json.dumps({
            "user": "fake_user_not_real",
            "password": "Example1"
        }), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertFalse(json.loads(response.content)['response'])
        self.assertEqual(json.loads(response.content)['reason'], "Invalid username or password")
