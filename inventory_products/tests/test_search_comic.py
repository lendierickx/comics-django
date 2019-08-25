from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls.static import static, settings
from inventory_products.views import search_comic
from inventory_base.tests.sample import SampleDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class ProductSearchComicTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_products.tests.test_search_comic
    """
    def tearDown(self):
        pass
        # Clear Sample Data
        populator = SampleDataPopulator()
        populator.dealloc()
    
    def setUp(self):
        # Create Sample Data
        populator = SampleDataPopulator()
        populator.populate()
    
    def test_url_resolves_to_search_comics_page(self):
        found = resolve('/inventory/1/1/comics')
        self.assertEqual(found.func, search_comic.search_comics_page)

    def test_url_resolves_to_search_products_page(self):
        found = resolve('/inventory/1/1/products/comics')
        self.assertEqual(found.func, search_comic.search_products_page)

    def test_search_comics_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/comics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b' Add',response.content)
        self.assertIn(b'<!-- Modal -->',response.content)

    def test_search_products_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/products/comics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'View',response.content)
        self.assertIn(b'Comics',response.content)