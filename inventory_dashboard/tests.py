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


class DashboardTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_dashboard.tests
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
    
    def test_url_resolves_to_dashboard(self):
        found = resolve('/inventory/1/1/dashboard')
        self.assertEqual(found.func, views.dashboard_page)

    def test_dashboard_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard',response.content)
        self.assertIn(b'<table ',response.content)