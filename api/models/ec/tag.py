from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from django.core.cache import caches


class Tag(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_tags'
    
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127)
    discount = models.DecimalField( # Note: Meaured in dollar ($) amount.
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    discount_type = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        choices=constants.PRODUCT_DISCOUNT_TYPE_OPTIONS,
        default=1,
    )
    organization = models.ForeignKey(Organization, db_index=True)
    
    def __str__(self):
        return str(self.tag_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Tag, self).save(*args, **kwargs)