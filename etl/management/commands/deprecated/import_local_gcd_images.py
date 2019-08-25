import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from etl.support.import_gcd.import_cover import *


LARGE_ZOOM = '4'
MEDIUM_ZOOM = '2'
SMALL_ZOOM = '1'
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2


class Command(BaseCommand):
    """
        -------------------------
        import_local_gcd_images
        -------------------------
        This ETL looks in the media/cover folder and iterates through all the
        images and creates the necessary cover database record. You would use
        this ETL if you already have all the images in the cover folder and you
        need to create/update the database.
        
        Run in your console:
        $ python manage.py import_local_gcd_images
    """
    help = 'Maps local issue covers to database records.'
    
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        
        # Check to see if the 'cover' directory has been created, if not
        # then lets create it.
        directory = settings.MEDIA_ROOT + '/cover/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Process all the images in the cover section.
        file_path = settings.MEDIA_ROOT + '/cover/'
        self.import_gcd(file_path)

    def begin_processing_image(self, full_file_path):
        """
            Function matches the file to model
        """
        # Process the filename to be used for extracting information
        directories = full_file_path.split("/")
        filename_with_ext = directories[-1]
        filename = filename_with_ext.split(".")
        filename = filename[0]
        id_array = filename.split("_")
        
        # Extract ID information
        issue_id = id_array[0]
        image_type = id_array[1]
        zoom = id_array[2]
    
        # Fetch the records we'll be using or create them
        try:
            issue = GCDIssue.objects.get(issue_id=issue_id)
        except GCDIssue.DoesNotExist:
            return  # Skip processing if issue doesn't exist.
        try:
            cover = Cover.objects.get(issue=issue)
            self.stdout.write('GCDLocalImageImporter: Updating: ' + issue_id)
        except Cover.DoesNotExist:
            cover = Cover.objects.create(issue=issue)
            self.stdout.write('GCDLocalImageImporter: Inserting: ' + issue_id)
                
        # Save images.
        file_path = settings.MEDIA_ROOT + '/cover/' + filename_with_ext
        if image_type is PRIMARY_IMAGE:
            if zoom is SMALL_ZOOM:
                cover.small = file_path
            if zoom is MEDIUM_ZOOM:
                cover.medium = file_path
            if zoom is LARGE_ZOOM:
                cover.large = file_path
        if image_type is ALTERNATIVE_IMAGE:
            cover.has_alternative = True
            if zoom is SMALL_ZOOM:
                cover.alt_small = file_path
            if zoom is MEDIUM_ZOOM:
                cover.alt_medium = file_path
            if zoom is LARGE_ZOOM:
                cover.alt_large = file_path
        cover.save()

    def get_filepaths(self, directory):
        """
            This function will generate the file names in a directory
            tree by walking the tree either top-down or bottom-up. For each
            directory in the tree rooted at directory top (including top itself),
            it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths = []  # List which will store all of the full filepaths.
                
        # Walk the tree.
        for root, directories, files in os.walk(directory):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.
        return file_paths  # Self-explanatory.

    def import_gcd(self, file_path):
        """
            Function looks at the current file_path and iterates through
            all the files in the directory and process each and individual
            file.
        """
        # Run the above function and store its results in a variable.
        full_file_paths = self.get_filepaths(file_path)
        
        for full_file_path in full_file_paths:
            for file_ext in [".png", ".jpeg", ".jpg", ".bmp", ".tiff"]:
                if full_file_path.endswith(file_ext):
                    self.begin_processing_image(full_file_path)
