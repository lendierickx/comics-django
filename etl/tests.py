import sys
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command


class PopulateTestCase(TestCase):
    """
        python manage.py test etl.tests
    """
    def tearDown(self):
        pass
    
    def setUp(self):
        pass
    
    def test_populate(self):
        """
            Test populating the database with sample data.
        """
        call_command('setup_sample_db')
