import json
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from inventory.tests.sample import SamplDataPopulator
from api.models.ec.imageupload import ImageUpload


# Notes:
# http://www.django-rest-framework.org/api-guide/testing/
# https://docs.python.org/3/library/unittest.html#unittest.TestCase


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"


class CustomerTests(APITestCase):
    """
        Run in Console:
        python manage.py test api.tests.test_customers
    """
    
    def tearDown(self):
        # Clear Sample Data
        populator = SamplDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        # Create Sample Data
        populator = SamplDataPopulator()
        populator.populate()
    
    def test_list_without_authentication(self):
        response = self.client.get('/api/customers/')
        json_string = response.content.decode(encoding='UTF-8')
        array = json.loads(json_string)
        self.assertEqual(array["detail"], 'Authentication credentials were not provided.')

    def test_list_with_success(self):
        self.client.login(username=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
        response = self.client.get('/api/customers/')
        json_string = response.content.decode(encoding='UTF-8')
        customers = json.loads(json_string)
        customer = customers[0]
        self.assertEqual(customer["first_name"], 'Rei')
        self.assertEqual(customer["last_name"], 'Ayanami')

    def test_post_with_success(self):
        # Fetch Our user.
        users = User.objects.all()
        user = users[0]
        
#        image = ImageUpload.objects.create(
#        )

        # Test.
        self.client.login(username=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
        response = self.client.post('/api/customers/', {
            'last_name': '111',
            'province': '222',
            'first_name': '333',
            'street_name': '444',
            'country': '555',
            'postal': '666',
            'email': '777@777.com',
            'phone': '888',
            'street_number': '777',
            'unit_number': '777',
            'city': '777',
            'province': '777',
            'country': '777',
            'user': user.id,
#            'profile': image.upload_id,
        })
        json_string = response.content.decode(encoding='UTF-8')
        customers = json.loads(json_string)
        
        # Verify.
        print(customers)

#        customer = customers[0]
#        self.assertEqual(customer["first_name"], 'Rei')
#        self.assertEqual(customer["last_name"], 'Ayanami')




