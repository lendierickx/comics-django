from django.db import models
from api.models.gcd.image import GCDImage
from api.models.gcd.brand import GCDBrand
from api.models.gcd.brandgroup import GCDBrandGroup


class GCDBrandEmblemGroup(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('brand',)
        db_table = 'gcd_brand_emblem_groups'
    
    brand_emblem_group_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(GCDBrand, null=True)
    brandgroup = models.ForeignKey(GCDBrandGroup, null=True)

    def __str__(self):
        return str(self.brand_emblem_group_id)
