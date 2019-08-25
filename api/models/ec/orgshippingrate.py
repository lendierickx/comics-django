from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ecantina_project import constants
from api.models.ec.organization import Organization
from django.core.cache import caches


class OrgShippingRate(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('country',)
        db_table = 'ec_org_shipping_rates'
    
    shipping_rate_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    
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
            super(OrgShippingRate, self).save(*args, **kwargs)

    def get_comics_rate(self,comics_count):
        """
            Function returns the specific rate for the comics count.
        """
        if comics_count > 0 and comics_count <= 10:
            return self.comics_rate1
        elif comics_count > 10 and comics_count <= 20:
            return self.comics_rate2
        elif comics_count > 20 and comics_count <= 30:
            return self.comics_rate3
        elif comics_count > 30 and comics_count <= 40:
            return self.comics_rate4
        elif comics_count > 40 and comics_count <= 50:
            return self.comics_rate5
        elif comics_count > 50 and comics_count <= 74:
            return self.comics_rate6
        elif comics_count > 74 and comics_count <= 100:
            return self.comics_rate7
        elif comics_count > 100 and comics_count <= 150:
            return self.comics_rate8
        elif comics_count > 150 and comics_count <= 200:
            return self.comics_rate9
        elif comics_count > 200 and comics_count <= 300:
            return self.comics_rate10
