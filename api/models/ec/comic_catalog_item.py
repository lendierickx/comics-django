from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.catalog import Catalog
from django.core.cache import caches


class ComicCatalogItem(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_comic_catalog_items'
    
    catalog_comic_id = models.AutoField(primary_key=True)
    catalog = models.ForeignKey(Catalog)
    
    # Issue identification
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
    
    # Price, page count and format fields
    price = models.CharField(max_length=255)
    page_count = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    page_count_uncertain = models.BooleanField(default=False)
    
    keywords = models.TextField(null=True, blank=True,)
    
    # Misc
    indicia_pub_not_printed = models.BooleanField(default=False)
    no_brand = models.BooleanField(default=False, db_index=True)
    
    # Foreign Keys
    images = models.ManyToManyField(GCDImage, blank=True)
    
    # Put them in here to simplify REST Framework
    publisher_name = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(CatalogComic, self).save(*args, **kwargs)
