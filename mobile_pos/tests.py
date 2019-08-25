import json

from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "password"


class CatalogTestCase(TestCase):
    def tearDown(self):
        pass
    
    def setUp(self):
        pass
    
    def test_url_resolves_to_catalog_page_view(self):
        found = resolve('/publish')
        self.assertEqual(found.func, catalog.catalog_page)
    
    def test_catalog_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/publish')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/publish',response.content)
        self.assertIn(b'Catalog',response.content)
