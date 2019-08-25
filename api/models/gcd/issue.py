from django.db import models
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.series import GCDSeries
from api.models.gcd.brand import GCDBrand


INDEXED = {
    'skeleton': 0,
    'full': 1,
    'partial': 2,
    'ten_percent': 3,
}


class GCDIssue(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ['series', 'sort_code']
        db_table = 'gcd_issues'

    # Issue identification
    issue_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    no_title = models.BooleanField(default=False, db_index=True)
    volume = models.CharField(max_length=50, db_index=True)
    no_volume = models.BooleanField(default=False, db_index=True)
    display_volume_with_number = models.BooleanField(default=False, db_index=True)
    isbn = models.CharField(max_length=32, db_index=True)
    no_isbn = models.BooleanField(default=False, db_index=True)
    valid_isbn = models.CharField(max_length=13, db_index=True)
    variant_of_id = models.IntegerField(default=0, db_index=True)
    variant_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=38, db_index=True)
    no_barcode = models.BooleanField(default=False)
    rating = models.CharField(max_length=255, default='', db_index=True)
    no_rating = models.BooleanField(default=False, db_index=True)
    is_first_issue = models.BooleanField(default=False)
    is_last_issue = models.BooleanField(default=False)

    # Dates and sorting
    publication_date = models.CharField(max_length=255)
    key_date = models.CharField(max_length=10, db_index=True)
    on_sale_date = models.CharField(max_length=10, db_index=True)
    on_sale_date_uncertain = models.BooleanField(default=False, blank=True)
    sort_code = models.IntegerField(db_index=True)
    indicia_frequency = models.CharField(max_length=255)
    no_indicia_frequency = models.BooleanField(default=False, db_index=True)

    # Price, page count and format fields
    price = models.CharField(max_length=255)
    page_count = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    page_count_uncertain = models.BooleanField(default=False)

    editing = models.TextField()
    no_editing = models.BooleanField(default=False, db_index=True)
    notes = models.TextField(null=True)

    keywords = models.TextField(null=True)

    # In production, this is a tinyint(1) because the set of numbers
    # is very small.  But syncdb produces an int(11).
    is_indexed = models.IntegerField(default=0, db_index=True)

    # Fields related to change management.
    reserved = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)

    # Misc
    indicia_pub_not_printed = models.BooleanField(default=False)
    no_brand = models.BooleanField(default=False, db_index=True)

    # Images
    small_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    medium_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    large_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    alt_small_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    alt_medium_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    alt_large_image = models.ImageField(
        upload_to='cover/issue',
        null=True,
        blank=True
    )
    has_alternative = models.BooleanField(default=False)

    # Foreign Keys
    brand = models.ForeignKey(GCDBrand, null=True)
    series = models.ForeignKey(GCDSeries, null=True)
    indicia_publisher = models.ForeignKey(GCDIndiciaPublisher, null=True)
    images = models.ManyToManyField(GCDImage, blank=True)

    # Put them in here to simplify REST Framework
    publisher_name = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    product_name = models.CharField(max_length=511, db_index=True, null=True, blank=True)

    # Functions
    def issue_descriptor(self):
        if self.number == '[nn]' and self.series.is_singleton:
            return u''
        if self.title and self.series.has_issue_title:
            title = u' - ' + self.title
        else:
            title = u''
        if self.display_volume_with_number:
            return u'v%s#%s%s' % (self.volume, self.number, title)
        return self.number + title

    def _display_number(self):
        number = self.issue_descriptor()
        if number:
            return u'#' + number
        else:
            return u''
        display_number = property(_display_number)

    def __str__(self):
        if self.variant_name:
            return u'%s %s [%s]' % (
                self.series,
                self._display_number(),
                self.variant_name
            )
        else:
            return u'%s %s' % (self.series, self._display_number())
