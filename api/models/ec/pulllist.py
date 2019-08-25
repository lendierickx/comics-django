from django.db import models
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.series import GCDSeries
from django.core.cache import caches


class Pulllist(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('series',)
        db_table = 'ec_pulllists'
    
    pulllist_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, db_index=True)
    store = models.ForeignKey(Store)
    series = models.ForeignKey(GCDSeries, null=True)
    
    def __str__(self):
        return str(self.series)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Pulllist, self).save(*args, **kwargs)