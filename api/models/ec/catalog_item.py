from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.imageupload import ImageUpload
from django.core.cache import caches


class CatalogItem(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_catalog_items'
    
    catalog_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True)
    type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=constants.PRODUCT_TYPE_OPTIONS,
        default=1,
        db_index=True,
    )
    description = models.TextField(default='', blank=True)
    brand_name = models.CharField(max_length=127, db_index=True)
    image = models.ForeignKey(ImageUpload, null=True, blank=True,)
    
    # Date & timekeeping tracking variables.
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Misc values
    length_in_meters = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
    )
    width_in_meters = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
    )
    height_in_meters = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
    )
    weight_in_kilograms = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
    )
    volume_in_litres = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
    )
    materials = models.CharField(max_length=127, null=True, blank=True,)
            
    # This indicates whether the product in the catalog is physical
    is_tangible = models.BooleanField(default=True)
      
    is_flammable = models.BooleanField(default=False)
    is_biohazard = models.BooleanField(default=False)
    is_toxic = models.BooleanField(default=False)
    is_explosive = models.BooleanField(default=False)
    is_corrosive = models.BooleanField(default=False)
    is_volatile = models.BooleanField(default=False)
    is_radioactive = models.BooleanField(default=False)
                    
    # Does the government have rules and regulations on selling this product?
    is_restricted = models.BooleanField(default=False)
    restrictions = models.TextField(default='', blank=True)
                    
    # Every catalog item is restricted to the domain belonging to the org/store.
    organization = models.ForeignKey(Organization)
    store = models.ForeignKey(Store, db_index=True)
                    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(CatalogItem, self).save(*args, **kwargs)
