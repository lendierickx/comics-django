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
        $ python manage.py load_gcd
    """
    help = 'Loads all the GCD model data from the fixtures.'
    
    def handle(self, *args, **options):
        # Clear the console text.
        os.system('clear;')
        self.stdout.write('Importing GCD.')
        
        # The filename of all the objects to be imported.
        ordered_file_names = [
            'gcd_brand.json',
            'gcd_brandemblemgroup.json',
            'gcd_brandgroup.json',
            'gcd_branduse.json',
            'gcd_country.json',
            'gcd_image.json',
            'gcd_indiciapublisher.json',
            'gcd_issue.json',
            'gcd_language.json',
            'gcd_publisher.json',
            'gcd_series.json',
            'gcd_story.json',
            'gcd_storytype.json',
        ]
                              
        # Iterate through all the filenames and load them into database.
        for file_name in ordered_file_names:
            call_command('loaddata', file_name)
        self.stdout.write('Finished Importing GCD.')
