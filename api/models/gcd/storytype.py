from django.db import models


class GCDStoryType(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('name',)
        db_table = 'gcd_story_types'
    
    story_type_id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=50, db_index=True, unique=True)
    sort_code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name