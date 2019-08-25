import json
from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

# Notes:
# https://docs.python.org/3/library/unittest.html#unittest.TestCase

class APITests(APITestCase):
    """
        Run in Console:
        python manage.py test api.tests.test_api
    """
    
    def test_api_root(self):
        response = self.client.get('/api/')
     
        # Verify: Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
    
        # Verify: Successful response.
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertIn('/api/customers/', array['customers'])
        self.assertIn('/api/carts/', array['carts'])
        self.assertIn('/api/products/', array['products'])
        self.assertIn('/api/employees/', array['employees'])

