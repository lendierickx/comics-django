from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls.static import static, settings
from . import views
from inventory_base.tests.sample import SampleDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class PullListTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_pulllist.tests
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
    
    def test_url_resolves_to_pulllist_page(self):
        found = resolve('/inventory/1/1/pulllist')
        self.assertEqual(found.func, views.pulllist_page)
    
    def test_url_resolves_to_pulllist_subscriptions_page(self):
        found = resolve('/inventory/1/1/pulllist/1/subscriptions')
        self.assertEqual(found.func, views.pulllist_subscriptions_page)
    
    def test_url_resolves_to_add_pulllist_page(self):
        found = resolve('/inventory/1/1/pulllist/add_pulllist')
        self.assertEqual(found.func, views.add_pulllist_page)
    
    def test_url_resolves_to_add_pulllist_customer_page(self):
        found = resolve('/inventory/1/1/pulllist/1/add_customer')
        self.assertEqual(found.func, views.add_pulllist_customer_page)

    def test_pulllist_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/pulllist')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pull List',response.content)
        self.assertIn(b'Winterworld',response.content)

    def test_pulllist_subscriptions_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/pulllist/1/subscriptions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'rayanami@nerv.worldgov',response.content)
        self.assertIn(b'Rei',response.content)

    def test_add_pulllist_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/pulllist/add_pulllist')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add New Pull List',response.content)
        self.assertIn(b'id_table_placeholder',response.content)

    def test_add_pulllist_customer_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/pulllist/1/add_customer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Customer',response.content)
        self.assertIn(b'Customer Details',response.content)