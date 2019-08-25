from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls.static import static, settings
from inventory_checkout.views import pos_item
from inventory_base.tests.sample import SampleDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class CheckoutItemTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_checkout.tests.test_pos_item
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
    
    def test_url_resolves_to_checkout_page(self):
        found = resolve('/inventory/1/1/checkout/1/items')
        self.assertEqual(found.func, pos_item.checkout_page)

    def test_url_resolves_to_content_page(self):
        found = resolve('/inventory/1/1/checkout/1/items/content')
        self.assertEqual(found.func, pos_item.content_page)
    
    def test_url_resolves_to_change_discount_type(self):
        found = resolve('/inventory/1/1/checkout/1/items/1/change_discount_type')
        self.assertEqual(found.func, pos_item.ajax_change_discount_type)

    def test_url_resolves_to_change_discount_amount(self):
        found = resolve('/inventory/1/1/checkout/1/items/1/change_discount_amount')
        self.assertEqual(found.func, pos_item.ajax_change_discount_amount)
    
    def test_url_resolves_to_change_tax(self):
        found = resolve('/inventory/1/1/checkout/1/items/change_tax')
        self.assertEqual(found.func, pos_item.ajax_change_tax)

    def test_url_resolves_to_verify(self):
        found = resolve('/inventory/1/1/checkout/1/items/verify')
        self.assertEqual(found.func, pos_item.ajax_verify)
    
    def test_url_resolves_to_process_receipt(self):
        found = resolve('/inventory/1/1/checkout/1/items/process_receipt')
        self.assertEqual(found.func, pos_item.ajax_process_receipt)

    def test_checkout_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/checkout/1/items')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Point of Sale',response.content)
        self.assertIn(b'Checkout',response.content)
        self.assertIn(b'id_content_placeholder',response.content)

    def test_content_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/checkout/1/items/content')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table',response.content)
        self.assertIn(b'Total',response.content)
        self.assertIn(b'GRAND TOTAL',response.content)

#-------
# TODO:
#-------
#url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/(\d+)/change_discount_type$', pos_item.ajax_change_discount_type),
#url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/(\d+)/change_discount_amount$', pos_item.ajax_change_discount_amount),
#url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/change_tax$', pos_item.ajax_change_tax),
#url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/verify$', pos_item.ajax_verify),
#url(r'^inventory/(\d+)/(\d+)/checkout/(\d+)/items/process_receipt$', pos_item.ajax_process_receipt),