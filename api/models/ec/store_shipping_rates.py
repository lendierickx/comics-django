from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches


class StoreShippingRate(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('country',)
        db_table = 'ec_store_shipping_rates'
    
    shipping_rate_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    store = models.ForeignKey(Store, db_index=True)
    country = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(840)],
        choices=constants.ISO_3166_1_NUMERIC_COUNTRY_CHOICES,
        null=True,
        blank=True,
    )
    comics_rate1 = models.DecimalField( # 1-10 Comics: $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate2 = models.DecimalField( # 11-20 Comics: $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate3 = models.DecimalField( # 21-30 Comics $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate4 = models.DecimalField( # 31-40 Comics $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate5 = models.DecimalField( # 41-50 Comics $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate6 = models.DecimalField( # 51-74 Comics $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate7 = models.DecimalField( # 75-100 Comics $___
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate8 = models.DecimalField( # 100-150 Comics $___
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )
    comics_rate9 = models.DecimalField( # 151-200 Comics $___
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )

    comics_rate10 = models.DecimalField( # 201-250 Comics $____
        max_digits=10,
        decimal_places=2,
        default=0.00,
        db_index=True
    )

    
    def __str__(self):
        return str(self.shipping_rate_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(StoreShippingRate, self).save(*args, **kwargs)
