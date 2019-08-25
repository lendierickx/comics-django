from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.orgshippingrate import OrgShippingRate
from django.core.cache import caches


class OrgShippingPreferenceManager(models.Manager):
    """
        Function will lookup and get the single OrgShippingPreference entry by 
        the id and if nothing was found, it will return a None object.
    """
    def get_by_org_or_none(self, organization):
        try:
            return self.get(organization=organization)
        except OrgShippingPreference.DoesNotExist:
            return None


class OrgShippingPreference(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('organization',)
        db_table = 'ec_org_shipping_preferences'
    
    objects = OrgShippingPreferenceManager()
    shipping_pref_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    is_pickup_only = models.BooleanField(default=False)
    rates = models.ManyToManyField(OrgShippingRate, blank=True, related_name='ord_shipping_rates', db_index=True)
    
    def __str__(self):
        return str(self.shipping_pref_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(OrgShippingPreference, self).save(*args, **kwargs)
