from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls.static import static, settings
from inventory_setting.views import employees
from inventory_base.tests.sample import SampleDataPopulator


# Contants
TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = TEST_USER_EMAIL
TEST_USER_PASSWORD = "password"

# Extra parameters to make this a Ajax style request.
KWARGS = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}


class EmployeeTestCase(TestCase):
    """
        Run in Console:
        python manage.py test inventory_setting.tests.test_employee
    """
    def tearDown(self):
        populator = SampleDataPopulator() # Clear Sample Data
        populator.dealloc()
    
    def setUp(self):
        populator = SampleDataPopulator() # Create Sample Data
        populator.populate()
    
    def test_url_resolves_to_listing_page(self):
        found = resolve('/inventory/1/1/settings/employee/1')
        self.assertEqual(found.func, employees.users_list_settings_page)
    
    def test_url_resolves_to_add_page(self):
        found = resolve('/inventory/1/1/settings/employee/new')
        self.assertEqual(found.func, employees.add_employee_page)
    
    def test_url_resolves_to_edit_page(self):
        found = resolve('/inventory/1/1/settings/employee/edit/1')
        self.assertEqual(found.func, employees.edit_user_settings_page)
    
    #    def test_url_resolves_to_assign_employee(self):
    #    found = resolve('/inventory/1/1/users/assign_employee')
    #    self.assertEqual(found.func, employees.ajax_assign_employee_to_store)

    def test_list_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/employee/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employees',response.content)
        self.assertIn(b'<table ',response.content)

    def test_add_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/employee/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employee Information',response.content)
        self.assertIn(b'id_hidden_upload_id',response.content)

    def test_edit_page_returns_correct_html(self):
        client = Client()
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.post('/inventory/1/1/settings/employee/edit/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employee Information',response.content)
        self.assertIn(b'id_hidden_upload_id',response.content)