import os
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import caches


UNASSIGNED_IMAGE_TYPE = 0
ASSIGNED_IMAGE_TYPE = 1

IMAGEUPLOAD_TYPE_OPTIONS = (
    UNASSIGNED_IMAGE_TYPE, 'Unassigned Image Type',
)


class ImageUpload(models.Model):
    class Meta:
        app_label = 'api'
        ordering = ('upload_date',)
        db_table = 'ec_image_uploads'
    
    upload_id = models.AutoField(primary_key=True)
    upload_date = models.DateField(auto_now=True, null=True)
    is_assigned = models.BooleanField(default=False)
    image = models.ImageField(upload_to='upload', null=True, blank=True)
    user = models.ForeignKey(User, null=True)
    
    def delete(self, *args, **kwargs):
        """
            Overrided delete functionality to include deleting the local file
            that we have stored on the system. Currently the deletion funciton
            is missing this functionality as it's our responsibility to handle
            the local files.
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(ImageUpload, self).delete(*args, **kwargs) # Call the "real" delete() method
    
    def __str__(self):
        return str(self.upload_id)

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(ImageUpload, self).save(*args, **kwargs)
