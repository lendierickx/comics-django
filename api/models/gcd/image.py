from django.db import models


class GCDImage(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'gcd_images'
    
    image_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255, db_index=True)
    file = models.FileField(upload_to='uploads',null=True)

    def __str__(self):
        return str(self.image_id)