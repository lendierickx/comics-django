from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.gcd.issue import GCDIssue
from api.models.gcd.series import GCDSeries
from api.models.gcd.image import GCDImage
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.imageupload import ImageUpload
from api.models.ec.product import Product
from api.models.ec.catalog_item import CatalogItem
from django.core.cache import caches


class Comic(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('issue',)
        db_table = 'ec_comics'
    
    comic_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    is_cgc_rated = models.BooleanField(default=False)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)],
        choices=constants.AGE_OPTIONS,
        null=True,
        blank=True,
    )
    cgc_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        choices=constants.CGC_RATING_OPTIONS,
        null=True,
        blank=True,
    )
    label_colour = models.CharField(
        max_length=63,
        choices=constants.LABEL_COLOUR_OPTIONS,
        null=True,
        blank=True,
    )
    condition_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        choices=constants.CONDITION_RATING_RATING_OPTIONS,
        null=True,
        blank=True,
    )
    is_canadian_priced_variant = models.BooleanField(default=False)
    is_variant_cover = models.BooleanField(default=False)
    is_retail_incentive_variant = models.BooleanField(default=False)
    is_newsstand_edition = models.BooleanField(default=False)
    
    organization = models.ForeignKey(Organization)
    product = models.ForeignKey(Product)
    
    # Developers Note: If the comic we are using is custom then the 'catalog'
    # field is to be filled, else we are to use the 'issue' field.
    issue = models.ForeignKey(GCDIssue, db_index=True, null=True, blank=True)
    catalog = models.ForeignKey(CatalogItem, db_index=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.issue)

    def delete(self, *args, **kwargs):
        """
            Deleting comic entry automatically deletes the foreign key.
        """
        if self.product:
            self.product.delete()
        super(Comic, self).delete(*args, **kwargs) # Call the "real" delete() method

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Comic, self).save(*args, **kwargs)
