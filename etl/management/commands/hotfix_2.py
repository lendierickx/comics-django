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
from ecantina_project.settings import env_var


class Command(BaseCommand):
    """
        $ python manage.py hotfix_imageurls
    """
    help = 'Remove old images which no longer exist..'


    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        self.stdout.write('Applying hotfix #2...')
        bucket_name = env_var("AWS_STORAGE_BUCKET_NAME")

        # Iterate through all the Comic Products and apply our new URL.
        try:
            products = Product.objects.filter(image_url__contains="www.comicscantina").order_by("product_id")
        except Comic.DoesNotExist:
            products = []

        for product in products.all():
            comic = Comic.objects.get(product_id=product.product_id)
            if comic.issue.large_image:
                print("Updating Product #", product.product_id)
                url = "https://s3.amazonaws.com/"+bucket_name+"/media/"+str(comic.issue.large_image)
                product.image_url = None
                product.save()
            else:
                print("Skipping Product #", product.product_id)
                product.image_url = None
                product.save()
