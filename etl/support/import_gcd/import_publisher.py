import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.country import GCDCountry
from api.models.gcd.publisher import GCDPublisher


class ImportPublisher:
    """
        Class is responsible for opening XML file and importing into database.
    """
    def __init__(self, file_path, has_formatting_requirements=False):
        self.file_path = file_path
        self.has_formatting_requirements = has_formatting_requirements

    def begin_import(self):
        if self.has_formatting_requirements:
            # Remove the text formating.
            fp = self.file_path
            os.system("tr -dc '[\011\012\015\040-\176\200-\377]' < "+fp+" > "+fp+"2;")
            os.system("mv "+fp+"2 "+fp+";")

        # Iterate through the contents of the file and import it.
        for event, elem in ET.iterparse(self.file_path):
            if elem.tag == "row":
                # Create an array holding all the row data.
                array = {}
                
                # Iterate through all the rows and save the items.
                for child in elem:
                    name = child.attrib['name']
                    text = child.text
                    array[name] = text
                
                # Import the data
                self.import_row(array)
                
                # Clear temp data.
                elem.clear()

    def import_row(self, array):
        #-----------#
        #  Extract  #
        #-----------#
        id = int(array['id'])
        name = array['name']
        country_id = int(array['country_id'])
        year_began = array['year_began']
        year_ended = array['year_ended']
        notes = array['notes']
        url = array['url']
        is_master = array['is_master']
        parent_id = array['parent_id']
        imprint_count = array['imprint_count']
        brand_count = array['brand_count']
        indicia_publisher_count = array['indicia_publisher_count']
        series_count = array['series_count']
        created = array['created']
        modified = array['modified']
        issue_count = array['issue_count']
        reserved = array['reserved']
        deleted = array['deleted']
        year_began_uncertain = array['year_began_uncertain']
        year_ended_uncertain = array['year_ended_uncertain']
        
        #-----------#
        # Transform #
        #-----------#
        try:
            country = GCDCountry.objects.get(country_id=country_id)
        except GCDCountry.DoesNotExist:
            country = None
    
        # Fix their weird data
        if year_began:
            year_began = 0 if year_began in 'NULL' else int(year_began)
            year_began = year_began if year_began <= 9999 else 0
            year_began = year_began if year_began >= 0 else 0

        if year_ended:
            year_ended = 0 if year_ended in 'NULL' else int(year_ended)
            year_ended = year_ended if year_ended <= 9999 else 0
            year_ended = year_ended if year_ended >= 0 else 0

        # Fix NULL entries into the name.
        if not name:
            name = ""

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDPublisher.objects.get(publisher_id=id)
            print("ImportPublisher: Updating: " + str(id))
            entry.name = name
            entry.year_began = year_began
            entry.year_ended = year_ended
            entry.notes = notes
            entry.url = url
            entry.is_master = is_master
            # entry.parent_id
            entry.imprint_count = imprint_count
            entry.brand_count = brand_count
            entry.indicia_publisher_count = indicia_publisher_count
            entry.series_count= series_count
            entry.created = created
            entry.modified = modified
            entry.issue_count = issue_count
            entry.reserved = reserved
            entry.deleted = deleted
            entry.year_began_uncertain = year_began_uncertain
            entry.year_ended_uncertain = year_ended_uncertain
            entry.country = country
            entry.save()
        except GCDPublisher.DoesNotExist:
            print("ImportPublisher: Inserting: " + str(id))
            GCDPublisher.objects.create(
                publisher_id=id,
                name=name,
                year_began=year_began,
                year_ended=year_ended,
                notes=notes,
                url=url,
                is_master=is_master,
                # parent_id
                imprint_count=imprint_count,
                brand_count=brand_count,
                indicia_publisher_count=indicia_publisher_count,
                series_count=series_count,
                created=created,
                modified=modified,
                issue_count=issue_count,
                reserved=reserved,
                deleted=deleted,
                year_began_uncertain=year_began_uncertain,
                year_ended_uncertain=year_ended_uncertain,
                country=country,
            )
