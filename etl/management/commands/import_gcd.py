import os
import sys
import re
import os.path as ospath
import codecs
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from etl.support.import_gcd.import_country import *
from etl.support.import_gcd.import_language import *
from etl.support.import_gcd.import_publisher import *
from etl.support.import_gcd.import_indiciapublisher import *
from etl.support.import_gcd.import_series import *
from etl.support.import_gcd.import_brandgroup import *
from etl.support.import_gcd.import_brand import *
from etl.support.import_gcd.import_issue import *
from etl.support.import_gcd.import_storytype import *
from etl.support.import_gcd.import_story import *

IMPORT_FILE_NAMES = [
    'gcd_country.xml',
    'gcd_language.xml',
    'gcd_publisher.xml',
    'gcd_indicia_publisher.xml',
    'gcd_series.xml' ,
    'gcd_issue.xml',
    'gcd_brand_group.xml',
    'gcd_brand.xml',
    'gcd_story_type.xml',
    'gcd_story.xml'
]


HAS_FORMATTING = False


class Command(BaseCommand):
    """
        ----------------------
        import_local_gcd
        ----------------------
        This ETL will load up all the *.xml files in the entered directory
        and iterate through them to import them into the database. Importing
        involves inserting new records or updating existing records.


        Run in your console:
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        python manage.py import_gcd /Users/bartlomiejmika/Developer/rodolfomartinez/comicscantina/gcd/xml
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    help = 'ETL loads up the GCD database into our applicaton using the provided xml files.'

    def strip_chars(self, f):
        remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]'
                               % u'')
        head,tail = ospath.split(f)
        fin = codecs.open(f, encoding = 'utf-8')
        fout = codecs.open(head + os.path.sep + 'tmp.xml', mode = 'w', encoding = 'utf-8')
        i = 1
        stripped = 0
        for line in fin:
            new_line, count = remove_re.subn('', line)
            if count > 0:
                plur = ((count > 1) and u's') or u''
                sys.stderr.write('Line %d, removed %s character%s.\n'
                                 % (i, count, plur))

            fout.write(new_line)
            stripped = stripped + count
            i = i + 1
        sys.stderr.write('Stripped %d characters from %d lines.\n'
                         % (stripped, i))
        fin.close()
        fout.close()
        os.rename(f, head + os.path.sep + 'old_' + tail)
        os.rename(head + os.path.sep + 'tmp.xml', f)

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+')

    def handle(self, *args, **options):
        os.system('clear;')  # Clear the console text.
        for file_path in options['file_path']:
            self.import_gcd(file_path)

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

    def begin_processing_xml(self, full_file_path):
        # Match the file names with the specific database imports


        if 'gcd_country.xml' in full_file_path:
            importer = ImportCountry(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_language.xml' in full_file_path:
            importer = ImportLanguage(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_publisher.xml' in full_file_path:
            importer = ImportPublisher(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_indicia_publisher.xml' in full_file_path:
            importer = ImportIndiciaPublisher(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_series.xml' in full_file_path:
            importer = ImportSeries(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_brand_group.xml' in full_file_path:
            importer = ImportBrandGroup(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_brand.xml' in full_file_path:
            importer = ImportBrand(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_issue.xml' in full_file_path:
            importer = ImportIssue(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_story_type.xml' in full_file_path:
            importer = ImportStoryType(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        if 'gcd_story.xml' in full_file_path:
            importer = ImportStory(full_file_path, HAS_FORMATTING)
            importer.begin_import()
        self.stdout.write('Imported "%s"' % full_file_path)

    def import_gcd(self, file_path):
        """
            Function looks at the current file_path and iterates through
            all the files in the directory and process each and individual
            file.
        """
        # Run the above function and store its results in a variable.
        full_file_paths = self.get_filepaths(file_path)

        # Import in order.
        for file_name in IMPORT_FILE_NAMES:
            for full_file_path in full_file_paths:
                if full_file_path.endswith(".xml"):
                    if file_name in full_file_path:
                        self.strip_chars(full_file_path)
                        self.begin_processing_xml(full_file_path)

        # Print Finish Message
        self.stdout.write('Importer Successfully Finished')
