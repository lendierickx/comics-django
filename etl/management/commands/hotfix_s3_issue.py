import os
import sys
import io
import requests
import hashlib
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


class Command(BaseCommand):
    help = 'ETL iterates all the Series and Issues, downloads them from a local running eCantina-Archive server and saves it to Amazon S3.'

    def add_arguments(self, parser):
        # Parameters control where we start and stop for Issue IDs.
        parser.add_argument('min_id', nargs='+', type=int)
        parser.add_argument('max_id', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        Main entry into this ETL. This is where the code will start running from.
        """
        os.system('clear;')  # Clear the console text.
        min_id = options['min_id'][0]
        max_id = options['max_id'][0]
        self.save_all_issues(min_id, max_id)

    def md5_for_file(self, f, block_size=2**20):
        """
        Returns the MD5 value of the file.

        Source: http://stackoverflow.com/a/1131255
        """
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.digest()

    def download_file(self, url):
        """
        Downloads the file to the filesystem.
        """
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
        # Source:
        #    https://vinta.ws/code/read-and-save-file-in-django-python.html
        #

    def delete_at_filepath(self, filepath):
        """
        Delete the file at this location.
        """
        if os.path.isfile(filepath):
            os.remove(filepath)

    def save_all_issues(self, min_id, max_id):
        """
        Save all issues.
        """
        # For debugging purposes only.
        # issues = GCDIssue.objects.filter(issue_id=1)

        # Code to use.
        issues = GCDIssue.objects.filter(
            issue_id__gte=min_id,
            issue_id__lte=max_id,
            #small_image__isnull=True  # Debugging Purposes: Return only non-processed images.
        ).order_by("issue_id")

        # Iterate through all the Issues and process them.
        for an_issue in issues.all():
            try:
                filename = str(an_issue.issue_id)

                # Small Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_1.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.small_image = None
                        an_issue.save()
                    else:
                        an_issue.small_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                # Medium Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_2.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.medium_image = None
                        an_issue.save()
                    else:
                        an_issue.medium_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                # Large Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_1_4.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.large_image = None
                        an_issue.save()
                    else:
                        an_issue.large_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                # Alt Small Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_1.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.alt_small_image = None
                        an_issue.save()
                    else:
                        an_issue.alt_small_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                # Alt Medium Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_2.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.alt_medium_image = None
                        an_issue.save()
                    else:
                        an_issue.alt_medium_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                # Alt Large Image
                url = IMAGE_SERVER_BASEL_URL + filename + "_2_4.jpg"
                filepath = self.download_file(url);
                with open(filepath, 'rb') as f:
                    md5 = self.md5_for_file(f)
                    if md5 == IMAGE_DOES_NOT_EXIST_MD5_CODE:
                        an_issue.alt_large_image = None
                        an_issue.save()
                    else:
                        an_issue.alt_large_image = File(f)
                        an_issue.save()
                        self.stdout.write(url + " - Saved")
                self.delete_at_filepath(filepath)

                self.stdout.write("Issue ID: " + str(an_issue.issue_id) + " - Saved")
            except GCDIssue.DoesNotExist:
                self.stdout.write("Issue ID: " + str(an_issue.issue_id) + " - Skipped")
