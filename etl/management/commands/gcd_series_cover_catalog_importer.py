import os
import sys
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models.gcd.series import GCDSeries


LARGE_ZOOM = 4
MEDIUM_ZOOM = 2
SMALL_ZOOM = 1
PRIMARY_IMAGE = 1
ALTERNATIVE_IMAGE = 2


class GCDSeriesCoverCatalogImporter:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def begin_import(self):
        print("Beginning importer")
        for event, elem in ET.iterparse(self.file_path):
            if elem.tag == "series":
                self.import_row(elem.attrib)
                elem.clear()

    def import_row(self, attrib):
        series_id = int(attrib['series_id'])
        url = attrib['url']
        
        print("GCDSeriesCoverCatalogImporter: Updating: " + str(series_id))
        try:
            series = GCDSeries.objects.get(series_id=series_id)
        except GCDSeries.DoesNotExist:
            print("Error: Series "+str(series_id)+" does not exist.")
            return
        series.cover_url = url
        series.save()

class Command(BaseCommand):
    """
        --------------------------------
        gcd_issue_cover_catalog_importer
        --------------------------------
        
        Run in your console:
        $ python manage.py gcd_series_cover_catalog_importer /Users/bartlomiejmika/Developer/ecantina/gcd/xml/series_catalog.xml
        
        (Where that file path is the path to where the GCD XML files are located)
    """
    help = 'ETL updates our applicaton with the latest series images using the provided xml files.'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+')
    
    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for full_file_path in options['file_path']:
            print("Opening:",full_file_path)
            importer = GCDSeriesCoverCatalogImporter(full_file_path)
            importer.begin_import()
        print("Successfully Imported")
