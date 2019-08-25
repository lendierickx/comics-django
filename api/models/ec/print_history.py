from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches


class PrintHistory(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('-created',)
        db_table = 'ec_print_history'
    
    print_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=127, db_index=True)
    url = models.URLField()
    store = models.ForeignKey(Store, db_index=True)
    organization = models.ForeignKey(Organization, db_index=True)
    
    def __str__(self):
        return str(self.filename)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(PrintHistory, self).save(*args, **kwargs)
