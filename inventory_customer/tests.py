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


class CustomerTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_customer.tests
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
    
    def test_url_resolves_to_customers_page(self):
        found = resolve('/inventory/1/1/customers')
        self.assertEqual(found.func, views.customers_page)
    
    def test_url_resolves_to_add_customer_page(self):
        found = resolve('/inventory/1/1/add_customer')
        self.assertEqual(found.func, views.add_customer_page)
    
    def test_url_resolves_to_profile_page(self):
        found = resolve('/inventory/1/1/customer/1/profile')
        self.assertEqual(found.func, views.profile_page)
    
    def test_url_resolves_to_purchases_page(self):
        found = resolve('/inventory/1/1/customer/1/purchases')
        self.assertEqual(found.func, views.purchases_page)
    
    def test_url_resolves_to_subscriptions_page(self):
        found = resolve('/inventory/1/1/customer/1/subscriptions')
        self.assertEqual(found.func, views.subscriptions_page)

    def test_customers_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customers',response.content)
        self.assertIn(b'id_table_placeholder',response.content)

    def test_add_customer_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/add_customer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Customer',response.content)
        self.assertIn(b'ajax_submit();',response.content)

    def test_profile_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customer/1/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile',response.content)
        self.assertIn(b'Account Information',response.content)
        self.assertIn(b'Addresses',response.content)
        self.assertIn(b'ajax_delete(1);',response.content)

    def test_purchases_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customer/1/purchases')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Purchases',response.content)
        self.assertIn(b'id_table_placeholder',response.content)


    def test_subscriptions_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/customer/1/subscriptions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Subscriptions',response.content)
        self.assertIn(b'<table ',response.content)