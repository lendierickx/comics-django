from django.db import models
from django.core.cache import caches


class BannedIP(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('address',)
        db_table = 'ec_banned_ips'
    
    id = models.AutoField(primary_key=True)
    address = models.GenericIPAddressField(db_index=True, unique=True)
    banned_on = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=127, blank=True, null=True)
    
    def __str__(self):
        return str(self.address)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(BannedIP, self).save(*args, **kwargs)
