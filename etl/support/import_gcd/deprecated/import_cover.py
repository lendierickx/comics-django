import os
import sys
import xml.etree.ElementTree as ET
import urllib3
from time import sleep
from bs4 import BeautifulSoup
import shutil
from django.conf import settings
from inventory.models.issue import GCDIssue
from inventory.models.cover import Cover

LARGE_ZOOM = '4'
MEDIUM_ZOOM = '2'
SMALL_ZOOM = '1'
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2
START_IMPORT_ARTIFICAL_DELAY = 2  # 2 Second delay
DOWNLOAD_IMAGE_ARTIFICAL_DELAY = 1

class ImportCover:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        # self.import_row(1278785)  #TEST CASE
        tree = ET.parse(self.file_path)
        database = tree.getroot()
        for table in database:
            for row in table:
                self.import_row(row)

    def detect_imagetype(self, url):
        if 'png' in url.lower():
            return 'png'
        if 'jpeg' in url.lower():
            return 'jpeg'
        if 'jpg' in url.lower():
            return 'jpg'
        if 'bmp' in url.lower():
            return 'bmp'
        if 'tiff' in url.lower():
            return 'tiff'
        if 'jfif' in url.lower():
            return 'jfif'
        if 'gif' in url.lower():
            return 'gif'
        return 'unknown'

    def import_row(self, row):
        # In order to prevent GCD for banning us for hammering their
        # system with our requests, we must add an artifical delay to
        # not raise any red flags.
        sleep(START_IMPORT_ARTIFICAL_DELAY)
        
        # Fetch the records we'll be using or create them
        issue_id = int(row.findtext('id'))
        try:
            issue = GCDIssue.objects.get(issue_id=issue_id)
        except GCDIssue.DoesNotExist:
            return
        try:
            cover = Cover.objects.get(issue=issue)
        except Cover.DoesNotExist:
            cover = Cover.objects.create(issue=issue)

        #-----------#
        #  Extract  #
        #-----------#
        # Handle making URL calls.
        http = urllib3.PoolManager()
        
        # GCD stores a copy of each image in three zoom levels. 4 is largest, 2
        # is medium and 1 is small.
        zoom_levels = [SMALL_ZOOM, MEDIUM_ZOOM , LARGE_ZOOM]
        
        for zoom in zoom_levels:
            r = http.request('GET', 'http://www.comics.org/issue/'+str(issue_id)+'/cover/'+zoom+'/')
            
            # Only process if a successful result was returned.
            if r.status == 200:
                # Scrap all the image files found on this page.
                soup = BeautifulSoup(r.data)
                images = soup.find_all('img',{'class':'cover_img'})
                
                # Variable controls whether image is primary or alternative.
                # Where 1 = Primary, 2 = Alternative
                file_index = PRIMARY_IMAGE
                
                # Iterate through all the scrapped image elements and save them locally.
                for image in images:
                    url = (image.get("src"))
                    print("Importing: " + url)

                    file_type = self.detect_imagetype(url)
                    file_name = str(issue_id) + '_' + str(file_index) + '_' + zoom
                    file_path = settings.MEDIA_ROOT + '/cover/' + file_name + '.' + file_type

                    #-----------#
                    # Transform #
                    #-----------#
                    # Save the image locally.
                    with http.request('GET', url, preload_content=False) as r, open(file_path, 'wb') as out_file:
                        shutil.copyfileobj(r, out_file)

                    #--------#
                    #  Load  #
                    #--------#
                    # Remove the full URL and only save up until "cover".
                    file_path = file_path.split("media/")[-1]
                    
                    # Save the location of the image based on what type it is.
                    if file_index is PRIMARY_IMAGE:
                        if zoom is SMALL_ZOOM:
                            cover.small = file_path
                        if zoom is MEDIUM_ZOOM:
                            cover.medium = file_path
                        if zoom is LARGE_ZOOM:
                            cover.large = file_path
                    if file_index is ALTERNATIVE_IMAGE:
                        cover.has_alternative = True
                        if zoom is SMALL_ZOOM:
                            cover.alt_small = file_path
                        if zoom is MEDIUM_ZOOM:
                            cover.alt_medium = file_path
                        if zoom is LARGE_ZOOM:
                            cover.alt_large = file_path
                    cover.save()

                    # Indicate we are now processing the alternative image
                    # on the next loop.
                    file_index = ALTERNATIVE_IMAGE

                    # Add an artifical delay in between downloads to prevent
                    # setting off any red-flags from GCD.
                    sleep(DOWNLOAD_IMAGE_ARTIFICAL_DELAY)
