from django.db import models
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.publisher import GCDPublisher


class GCDSeries(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ['sort_name', 'year_began']
        db_table = 'gcd_series'

    # Core series fields.
    series_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    sort_name = models.CharField(max_length=255, db_index=True)

    # The "format" field is a legacy field that is being split into
    # color, dimensions, paper_stock, binding, and publishing_format
    format = models.CharField(max_length=255, default=u'')
    color = models.CharField(max_length=255, default=u'')
    dimensions = models.CharField(max_length=255, default=u'')
    paper_stock = models.CharField(max_length=255, default=u'')
    binding = models.CharField(max_length=255, default=u'')
    publishing_format = models.CharField(max_length=255, default=u'')

    tracking_notes = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    publication_notes = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)

    year_began = models.IntegerField(db_index=True)
    year_ended = models.IntegerField(null=True, default=0, blank=True)
    year_began_uncertain = models.BooleanField(default=False, blank=True)
    year_ended_uncertain = models.BooleanField(default=False, blank=True)
    publication_dates = models.CharField(max_length=255)

    # Fields for handling the presence of certain issue fields
    has_barcode = models.BooleanField(default=False)
    has_indicia_frequency = models.BooleanField(default=False)
    has_isbn = models.BooleanField(default=False)
    has_issue_title = models.BooleanField(default=False)
    has_volume = models.BooleanField(default=False)
    has_rating = models.BooleanField(default=False)

    is_current = models.BooleanField(default=False)
    is_comics_publication = models.BooleanField(default=False)
    is_singleton = models.BooleanField(default=False)
    issue_count = models.IntegerField(null=True, default=0, blank=True)

    # Fields related to cover image galleries.
    has_gallery = models.BooleanField(default=False, db_index=True)

    # Fields related to indexing activities.
    # Only "reserved" is in active use.  "open_reserve" is a legacy field
    # used only by migration scripts.
    reserved = models.BooleanField(default=False, db_index=True)
    open_reserve = models.IntegerField(null=True)

    # Fields related to change management.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False, db_index=True)

    # Country and Language info.
    country = models.ForeignKey(
        GCDCountry,
        blank=True,
        null=True
    )
    language = models.ForeignKey(
        GCDLanguage,
        blank=True,
        null=True
    )

    # Cover
    cover = models.ImageField(
        upload_to='cover/series',
        null=True,
        blank=True
    )

    # Fields related to the publishers table.
    publication_type_id = models.IntegerField(null=True, blank=0)
    publisher = models.ForeignKey(GCDPublisher)
    images = models.ManyToManyField(GCDImage, blank=True)

    # Put them in here to simplify REST Framework
    publisher_name = models.CharField(max_length=255, db_index=True)

    def _date_uncertain(self, flag):
        return u' ?' if flag else u''

    def __str__(self):
        return '%s (%s%s series)' % (self.name, self.year_began, self._date_uncertain(self.year_began_uncertain))
