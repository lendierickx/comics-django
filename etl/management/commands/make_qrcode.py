import os
import sys
import qrcode
from PIL import Image
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from ecantina_project import constants


class Command(BaseCommand):
    help = 'Function will generate QR-code in the /media/qrcode file for the entered integer.'
    
    def add_arguments(self, parser):
        parser.add_argument('product_id', nargs='+')
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        
        for product_id in options['product_id']:
            filepath = 'qrcode/'+str(product_id)+'.jpeg'
        
            # Generate QRCode Image and save it locally.
            img = qrcode.make(product_id)
            img.save(os.path.join(settings.MEDIA_ROOT,filepath), 'JPEG')

        # Finish Message!
        self.stdout.write('QR Code(s) generated')
