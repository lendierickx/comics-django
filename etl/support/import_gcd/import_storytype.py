import os
import sys
import xml.etree.ElementTree as ET
from django.conf import settings
from api.models.gcd.storytype import GCDStoryType


class ImportStoryType:
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
        sort_code = array['sort_code']

        #-----------#
        # Transform #
        #-----------#
    
        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDStoryType.objects.get(story_type_id=id)
            print("ImportStoryType: Updating: " + str(id))
            entry.name = name
            entry.sort_code = sort_code
            entry.save()
        except GCDStoryType.DoesNotExist:
            print("ImportStoryType: Inserting: " + str(id))
            GCDStoryType.objects.create(
                story_type_id=id,
                name=name,
                sort_code=sort_code,
            )