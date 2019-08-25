from django.db import models
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from django.core.cache import caches


class Section(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_sections'
    
    section_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=127, db_index=True)
    store = models.ForeignKey(Store, db_index=True)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Section, self).save(*args, **kwargs)