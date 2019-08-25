import os
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.conf import settings
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.issue import GCDIssue


INITIAL_ID_NUMBER = 1489230  # Set what value to start the ETL import to.


class ImportStory:
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
                if int(array['id']) >= INITIAL_ID_NUMBER:
                    self.import_row(array)
                
                # Clear temp data.
                elem.clear()

    def import_row(self, array):
        #-----------#
        #  Extract  #
        #-----------#
        id = int(array['id'])
        title = array['title']
        title_inferred = array['title_inferred']
        feature = array['feature']
        sequence_number = array['sequence_number']
        page_count = array['page_count']
        issue_id = array['issue_id']
        script = array['script']
        pencils = array['pencils']
        inks = array['inks']
        colors = array['colors']
        letters = array['letters']
        editing = array['editing']
        genre = array['genre']
        characters = array['characters']
        synopsis = array['synopsis']
        reprint_notes = array['reprint_notes']
        created = array['created']
        modified = array['modified']
        notes = array['notes']
        no_script = array['no_script']
        no_pencils = array['no_pencils']
        no_inks = array['no_inks']
        no_colors = array['no_colors']
        no_letters = array['no_letters']
        no_editing = array['no_editing']
        page_count_uncertain = array['page_count_uncertain']
        type_id = array['type_id']
        job_number = array['job_number']
        reserved = array['reserved']
        deleted = array['deleted']
        
        # Protected extract.
        try:
            name = array['name']
        except Exception as e:
            name = ""

        #-----------#
        # Transform #
        #-----------#
        if page_count:
            page_count = 0 if page_count in 'NULL' else Decimal(page_count)

        try:
            story_type = GCDStoryType.objects.get(story_type_id = type_id)
        except GCDStoryType.DoesNotExist:
            story_type = None

        try:
            issue = GCDIssue.objects.get(issue_id = issue_id)
        except GCDIssue.DoesNotExist:
            issue = None
        
        if not name:
            name = ""
        
        if not editing:
            editing = ""
        
        if not job_number:
            job_number = ""

        if not characters:
            characters = ""

        if not synopsis:
            synopsis = ""

        if not reprint_notes:
            reprint_notes = ""

        if not notes:
            notes = ""

        if not script:
            script = ""

        if not feature:
            feature = ""

        if not genre:
            genre = ""

        if not title:
            title = ""

        if not letters:
            letters = ""

        if not pencils:
            pencils = ""

        if not inks:
            inks = ""

        if not title_inferred:
            title_inferred = ""

        if not colors:
            colors = ""

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDStory.objects.get(story_id=id)
            print("ImportStory: Updating Story: " + str(id))
            entry.save()
        except GCDStory.DoesNotExist:
            print("ImportStory: Inserting Story: " + str(id))
            GCDStory.objects.create(
                story_id=id,
                title = title,
                title_inferred = title_inferred,
                feature = feature,
                sequence_number = sequence_number,
                page_count = page_count,
                issue = issue,
                script = script,
                pencils = pencils,
                inks = inks,
                colors = colors,
                letters = letters,
                editing = editing,
                genre = genre,
                characters = characters,
                synopsis = synopsis,
                reprint_notes = reprint_notes,
                created = created,
                modified = modified,
                notes = notes,
                no_script = no_script,
                no_pencils = no_pencils,
                no_inks = no_inks,
                no_colors = no_colors,
                no_letters = no_letters,
                no_editing = no_editing,
                page_count_uncertain = page_count_uncertain,
                type = story_type,
                job_number = job_number,
                reserved = reserved,
                deleted = deleted,
            )
        
        # Updated Issue
        print("ImportStory: Updating Issue: " + str(issue_id))
        issue.genre = genre
        issue.save()
