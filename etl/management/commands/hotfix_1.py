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

PNG_EXTENSION = 'png'
JPG_EXTENSION = 'jpg'
JPEG_EXTENSION = 'jpeg'
TIFF_EXTENSION = 'tiff'
JFIF_EXTENSION = 'jfif'
GIF_EXTENSION = 'gif'
BMP_EXTENSION = 'bmp'
UNKNOWN_EXTENSION = 'unknown'

def detect_imagetype(url):
    if PNG_EXTENSION in url.lower():
        return PNG_EXTENSION
        if JPEG_EXTENSION in url.lower():
            return JPEG_EXTENSION
    if JPG_EXTENSION in url.lower():
        return JPG_EXTENSION
        if BMP_EXTENSION in url.lower():
            return BMP_EXTENSION
    if TIFF_EXTENSION in url.lower():
        return TIFF_EXTENSION
        if JFIF_EXTENSION in url.lower():
            return JFIF_EXTENSION
    if GIF_EXTENSION in url.lower():
        return GIF_EXTENSION
    return UNKNOWN_EXTENSION


class Command(BaseCommand):
    """
        $ python manage.py hotfix_imageurls
    """
    help = 'Makes all series/issues/products/comics have new URLs.'
    
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        self.stdout.write('Applying hotfix #1...')
        
        # Iterate through all the Comic Products and apply our new URL.
        try:
            comics = Comic.objects.all().order_by("product_id")
        except Comic.DoesNotExist:
            comics = []
        
        for comic in comics:
            issue_id = comic.issue_id
            self.stdout.write("Fixing Comic at Issue #"+ str(issue_id))
            
            # Detect non-custom image.
            if "media" not in comic.product.image_url:
                img_type = detect_imagetype(comic.product.image_url)
                comic.product.image_url = "https://comicscantina.com/img/"+str(issue_id)+"_1_4."+str(img_type)
                comic.product.save()
    
        # Iterate through all the Series and apply our new URL.
        try:
            series = GCDSeries.objects.all().order_by("series_id")
        except GCDSeries.DoesNotExist:
            series = []
            
        for a_series in series:
            series_id = a_series.series_id
            img_type = detect_imagetype(a_series.cover_url)
            self.stdout.write("Fixing Series #" + str(series_id))
            filename = str(series_id)+"."+str(img_type)
            a_series.cover_url = "https://comicscantina.com/img/"+filename
            a_series.save()

        # Iterate through all the Issues and apply our new URL
        try:
            issues = GCDIssue.objects.all().order_by("issue_id")
        except GCDIssue.DoesNotExist:
            issues = []

        for issue in issues:
            issue_id = issue.issue_id
            self.stdout.write("Fixing Issue #"+ str(issue_id))
            img_type = detect_imagetype(issue.small_url)
            issue.small_url = "https://comicscantina.com/img/"+str(issue_id)+"_1_1."+str(img_type)
            img_type = detect_imagetype(issue.medium_url)
            issue.medium_url = "https://comicscantina.com/img/"+str(issue_id)+"_1_2."+str(img_type)
            img_type = detect_imagetype(issue.large_url)
            issue.large_url = "https://comicscantina.com/img/"+str(issue_id)+"_1_4."+str(img_type)
            img_type = detect_imagetype(issue.alt_small_url)
            issue.alt_small_url = "https://comicscantina.com/img/"+str(issue_id)+"_2_1."+str(img_type)
            img_type = detect_imagetype(issue.alt_medium_url)
            issue.alt_medium_url = "https://comicscantina.com/img/"+str(issue_id)+"_2_2."+str(img_type)
            img_type = detect_imagetype(issue.alt_large_url)
            issue.alt_large_url = "https://comicscantina.com/img/"+str(issue_id)+"_2_4."+str(img_type)
            issue.save()

        # Finish Message!
        self.stdout.write('Hotfix #1 successfully applied!')
