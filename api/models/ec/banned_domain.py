from django.db import models
from django.core.cache import caches


class BannedDomain(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_banned_domains'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(BannedDomain, self).save(*args, **kwargs)
