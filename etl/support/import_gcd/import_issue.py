import os
import sys
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.conf import settings
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue


INITIAL_ID_NUMBER = 0  # Set what value to start the ETL import to.


class ImportIssue:
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

                if int(array['id']) >= INITIAL_ID_NUMBER:
                    self.import_row(array)

                # Clear temp data.
                elem.clear()

    def import_row(self, array):
        #-----------#
        #  Extract  #
        #-----------#
        id = int(array['id'])
        number = array['number']
        volume = array['volume']
        no_volume = array['no_volume']
        display_volume_with_number = array['display_volume_with_number']
        series_id = array['series_id']
        indicia_publisher_id = array['indicia_publisher_id']
        indicia_pub_not_printed = array['indicia_pub_not_printed']
        brand_id = array['brand_id']
        no_brand = array['no_brand']
        publication_date = array['publication_date']
        key_date = array['key_date']
        sort_code = array['sort_code']
        price = array['price']
        page_count = array['page_count']
        page_count_uncertain = array['page_count_uncertain']
        indicia_frequency = array['indicia_frequency']
        no_indicia_frequency = array['no_indicia_frequency']
        editing = array['editing']
        no_editing = array['no_editing']
        notes = array['notes']
        created = array['created']
        modified = array['modified']
        reserved = array['reserved']
        deleted = array['deleted']
        is_indexed = array['is_indexed']
        isbn = array['isbn']
        valid_isbn = array['valid_isbn']
        no_isbn = array['no_isbn']
        variant_of_id = array['variant_of_id']
        variant_name = array['variant_name']
        barcode = array['barcode']
        no_barcode = array['no_barcode']
        title = array['title']
        no_title = array['no_title']
        on_sale_date = array['on_sale_date']
        on_sale_date_uncertain = array['on_sale_date_uncertain']
        rating = array['rating']
        no_rating = array['no_rating']

        #-----------#
        # Transform #
        #-----------#
        if brand_id is None:
            brand_id = 0
        else:
            brand_id = 0 if brand_id in 'NULL' else int(brand_id)

        if series_id:
            series_id = 0 if series_id in 'NULL' else int(series_id)

        if indicia_publisher_id:
            indicia_publisher_id = 0 if indicia_publisher_id in 'NULL' else int(indicia_publisher_id)

        if variant_of_id:
            variant_of_id = 0 if variant_of_id in 'NULL' else int(variant_of_id)

        if page_count:
            page_count = 0 if page_count in 'NULL' else Decimal(page_count)

        if is_indexed:
            is_indexed = False if is_indexed in 'NULL' else int(is_indexed)

        if not title:
            title = ""

        if not volume:
            volume = ""

        if not isbn:
            isbn = ""

        if not valid_isbn:
            valid_isbn = ""

        if not variant_of_id:
            variant_of_id = 0

        if not variant_name:
            variant_name = ""

        if not barcode:
            barcode = ""

        if not rating:
            rating = ""

        if not indicia_frequency:
            indicia_frequency = ""

        if not on_sale_date:
            on_sale_date = ""

        if not price:
            price = ""

        if not editing:
            editing = ""

        if not publication_date:
            publication_date = ""

        if not key_date:
            key_date = ""

        if not key_date:
            key_date = ""

        if not number:
            number = "0"

        no_title = True if no_title is '1' else False
        no_volume = True if no_volume is '1' else False
        display_volume_with_number = True if display_volume_with_number is '1' else False
        no_isbn = True if no_isbn is '1' else False
        no_barcode = True if no_barcode is '1' else False
        on_sale_date_uncertain = True if on_sale_date_uncertain is '1' else False
        no_rating = True if no_rating is '1' else False
        no_indicia_frequency = True if no_indicia_frequency is '1' else False
        no_editing = True if no_editing in '1' else False
        reserved = True if reserved in '1' else False
        indicia_pub_not_printed = True if indicia_pub_not_printed in '1' else False
        no_brand = True if no_brand in '1' else False
        deleted = True if deleted in '1' else False

        try:
            indicia_publisher = GCDIndiciaPublisher.objects.get(indicia_publisher_id=indicia_publisher_id)
        except GCDIndiciaPublisher.DoesNotExist:
            indicia_publisher = None

        try:
            series = GCDSeries.objects.get(series_id=series_id)
            publisher_name = series.publisher_name # (Assumption: Series ETL ran before Issues ETL)
        except GCDSeries.DoesNotExist:
            series = None
            publisher_name = ""

        try:
            brand = GCDBrand.objects.get(brand_id=brand_id)
        except GCDBrand.DoesNotExist:
            brand = None

        # Generate URL for images.
        base_url = settings.COMICS_CANTINA_IMAGE_SERVER_BASE_URL
        #small_url = base_url + str(id) + '_1_1.jpg'
        #medium_url = base_url + str(id) + '_1_2.jpg'
        #large_url = base_url + str(id) + '_1_4.jpg'
        #alt_small_url = base_url + str(id) + '_2_1.jpg'
        #alt_medium_url = base_url + str(id) + '_2_2.jpg'
        #alt_large_url = base_url + str(id) + '_2_4.jpg'
        has_alternative = False

        #--------#
        #  Load  #
        #--------#
        # Check to see if record already exists for the given identification.
        try:
            entry = GCDIssue.objects.get(issue_id=id)
            print("ImportIssue: Updating: " + str(id))
            entry.number = number
            entry.volume = volume
            entry.no_volume = no_volume
            entry.display_volume_with_number = display_volume_with_number
            entry.series = series
            entry.indicia_publisher = indicia_publisher
            entry.indicia_pub_not_printed = indicia_pub_not_printed
            entry.brand = brand
            entry.no_brand = no_brand
            entry.publication_date = publication_date
            entry.key_date = key_date
            entry.sort_code = sort_code
            entry.price = price
            entry.page_count = page_count
            entry.page_count_uncertain = page_count_uncertain
            entry.indicia_frequency = indicia_frequency
            entry.no_indicia_frequency = no_indicia_frequency
            entry.editing = editing
            entry.no_editing = no_editing
            entry.notes = notes
            entry.created = created
            entry.modified = modified
            entry.reserved = reserved
            entry.deleted = deleted
            entry.is_indexed = is_indexed
            entry.isbn = isbn
            entry.valid_isbn = valid_isbn
            entry.no_isbn = no_isbn
            entry.variant_of_id = variant_of_id
            entry.variant_name = variant_name
            entry.barcode = barcode
            entry.no_barcode = no_barcode
            entry.title = title
            entry.no_title = no_title
            entry.on_sale_date = on_sale_date
            entry.on_sale_date_uncertain = on_sale_date_uncertain
            entry.rating = rating
            entry.no_rating = no_rating
            entry.publisher_name = publisher_name
            # entry.small_url = small_url
            # entry.medium_url = medium_url
            # entry.large_url = large_url
            # entry.alt_small_url = alt_small_url
            # entry.alt_medium_url = alt_medium_url
            # entry.alt_large_url = alt_large_url
            entry.has_alternative = has_alternative
            entry.save()
        except GCDIssue.DoesNotExist:
            print("ImportIssue: Inserting: " + str(id))
            entry = GCDIssue.objects.create(
                issue_id=id,
                number=number,
                volume = volume,
                no_volume = no_volume,
                display_volume_with_number = display_volume_with_number,
                series = series,
                indicia_publisher = indicia_publisher,
                indicia_pub_not_printed = indicia_pub_not_printed,
                brand = brand,
                no_brand = no_brand,
                publication_date = publication_date,
                key_date = key_date,
                sort_code = sort_code,
                price = price,
                page_count = page_count,
                page_count_uncertain = page_count_uncertain,
                indicia_frequency = indicia_frequency,
                no_indicia_frequency = no_indicia_frequency,
                editing = editing,
                no_editing = no_editing,
                notes = notes,
                created = created,
                modified = modified,
                reserved = reserved,
                deleted = deleted,
                is_indexed = is_indexed,
                isbn = isbn,
                valid_isbn = valid_isbn,
                no_isbn = no_isbn,
                variant_of_id = variant_of_id,
                variant_name = variant_name,
                barcode = barcode,
                no_barcode = no_barcode,
                title = title,
                no_title = no_title,
                on_sale_date = on_sale_date,
                on_sale_date_uncertain = on_sale_date_uncertain,
                rating = rating,
                no_rating = no_rating,
                publisher_name=publisher_name,
                # small_url = small_url,
                # medium_url = medium_url,
                # large_url = large_url,
                # alt_small_url = alt_small_url,
                # alt_medium_url = alt_medium_url,
                # alt_large_url = alt_large_url,
                has_alternative = has_alternative,
            )

        # Update the product name of the issue.
        entry.product_name = str(entry)
        entry.save()
