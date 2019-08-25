from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.store_shipping_rates import StoreShippingRate
from django.core.cache import caches

class StoreShippingPreference(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('organization',)
        db_table = 'ec_store_shipping_preferences'
    
    shipping_pref_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    store = models.ForeignKey(Store, db_index=True)
    is_pickup_only = models.BooleanField(default=False)
    rates = models.ManyToManyField(StoreShippingRate, blank=True, related_name='store_shipping_rates', db_index=True)
    
    def __str__(self):
        return str(self.shipping_pref_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(StoreShippingPreference, self).save(*args, **kwargs)
