from django.db import models
from api.models.gcd.image import GCDImage
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand

class GCDBrandUse(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('publisher',)
        db_table = 'gcd_brand_uses'
    
    brand_use_id = models.AutoField(primary_key=True)
    publisher = models.ForeignKey(GCDPublisher)
    emblem = models.ForeignKey(GCDBrand, related_name='in_use')
    
    year_began = models.IntegerField(db_index=True, null=True)
    year_ended = models.IntegerField(null=True)
    year_began_uncertain = models.BooleanField(blank=True, db_index=True)
    year_ended_uncertain = models.BooleanField(blank=True, db_index=True)
    
    notes = models.TextField()
    
    # Fields related to change management.
    reserved = models.BooleanField(default=0, db_index=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name