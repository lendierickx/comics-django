import os
import sys
from datetime import datetime
from django.db import connection, transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ecantina_project import constants
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from django.core.management import call_command


class Command(BaseCommand):
    """
        $ python manage.py dump_gcd
    """
    help = 'Dumps all the GCD model data into a specific folder.'
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        self.stdout.write('Bumping GCD.')  # Indicated we begin.
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directory = directory.replace("/etl/management", "/etl/fixtures")
        self.begin_export(directory)  # Run the ETL.
        self.stdout.write('Finished dumping GCD.')  # Indicate we are finished.

    def begin_export(self, directory):
        # List all the items to be exported.
        model_names = [
            'api.GCDBrand',
            'api.GCDBrandEmblemGroup',
            'api.GCDBrandGroup',
            'api.GCDBrandUse',
            'api.GCDCountry',
            'api.GCDImage',
            'api.GCDIndiciaPublisher',
            'api.GCDIssue',
            'api.GCDLanguage',
            'api.GCDPublisher',
            'api.GCDSeries',
            'api.GCDStory',
            'api.GCDStoryType',
        ]
        
        # Iterate through all the Models that we want to export into a file.
        for model_name in model_names:
            # Create the filename.
            file_name = model_name.replace('api.GCD','gcd_').lower()
            
            # Create the filepath.
            file_path = directory +'/' + file_name + '.json'
           
            # Export the data to the file.
            with open(file_path, 'w') as f:
                call_command('dumpdata', model_name, stdout=f)
