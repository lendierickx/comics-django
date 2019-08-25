import os
import sys
import io
import requests
import hashlib
from time import sleep
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.ec.comic import Comic
from api.models.ec.product import Product
from ecantina_project.settings import env_var


IMAGE_SERVER_BASEL_URL = "http://127.0.0.1:8000/image/"
IMAGE_DOES_NOT_EXIST_MD5_CODE = b'\xdaY\xbb\x93\x13\xc9\x14N\xfa\xd0\x86\xbf\x10\x85\xb7\x87'
SYNC_ARTIFICAL_DELAY = 0 # (measured in seconds)


class Command(BaseCommand):
    help = 'ETL iterates all the Series and Issues, downloads them from a local running eCantina-Archive server and saves it to Amazon S3.'

    def handle(self, *args, **options):
        """
        Main entry into this ETL. This is where the code will start running from.
        """
        os.system('clear;')  # Clear the console text.
        self.update_all_products()

    def update_all_products(self):
        """
        Iterate through all the Products and update their product image.
        """
        # Fetch all the products we have in our inventory and update their
        # images depending on whether it's an uploaded image or a GCD image.
        products = Product.objects.all()
        for a_product in products.all():
            if 'www.comicscantina.com' in a_product.image_url:
                self.stdout.write(a_product.image_url + "- OLD RECORD SKIPPED")

            if 'upload' in a_product.image_url:
                # Save the image(s) uploaded.
                if a_product.image:
                    url = "https://s3.amazonaws.com/"+bucket_name+"/media/"+str(a_product.image.image)
                    a_product.image_url = url
                    a_product.save()
                    self.stdout.write(url + "- Saved")
            else:
                comic = Comic.objects.get(product=a_product)
                if comic.issue.small_image:
                    bucket_name = env_var("AWS_STORAGE_BUCKET_NAME")
                    url = "https://s3.amazonaws.com/"+bucket_name+"/media/"+str(comic.issue.large_image)
                    a_product.image_url = url
                    a_product.save()
                    self.stdout.write(url + "- Saved")
