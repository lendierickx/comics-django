from django.db import models
from api.models.gcd.image import GCDImage
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup


class GCDBrand(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'gcd_brands'
    
    brand_id = models.AutoField(primary_key=True)
    issue_count = models.IntegerField(default=0)
    parent = models.ForeignKey(GCDPublisher, null=True)
    group = models.ManyToManyField(
        GCDBrandGroup, blank=True,
        db_table='gcd_brand_emblem_group',
    )
    images = models.ManyToManyField(GCDImage, blank=True)

    # Core publisher fields.
    name = models.CharField(max_length=255, db_index=True)
    year_began = models.IntegerField(db_index=True, null=True)
    year_ended = models.IntegerField(null=True)
    year_began_uncertain = models.BooleanField(blank=True, db_index=True)
    year_ended_uncertain = models.BooleanField(blank=True, db_index=True)
    notes = models.TextField()
    keywords = models.TextField(null=True)
    url = models.URLField(max_length=255, blank=True, default=u'')
    
    # Fields related to change management.
    reserved = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.name