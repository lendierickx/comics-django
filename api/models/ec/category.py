from django.db import models
from django.core.validators import MinValueValidator
from api.models.ec.organization import Organization
from django.core.cache import caches


class Category(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'ec_categories'
    
    category_id = models.AutoField(primary_key=True)
    parent_id = models.PositiveIntegerField(
        default=0,
    )
    name = models.CharField(max_length=127)
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(Category, self).save(*args, **kwargs)
