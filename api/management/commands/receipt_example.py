import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'ETL for example.
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        
