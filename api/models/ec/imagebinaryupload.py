import os
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import caches

PNG_EXTENSION = 'png'
JPG_EXTENSION = 'jpg'
JPEG_EXTENSION = 'jpeg'
TIFF_EXTENSION = 'tiff'
JFIF_EXTENSION = 'jfif'
GIF_EXTENSION = 'gif'
BMP_EXTENSION = 'bmp'
UNKNOWN_EXTENSION = 'unknown'

SUPPORTED_FILE_EXTENSIONS = ['.png', '.jpeg',  '.jpg',  '.bmp',  '.tiff', '.gif']

IMAGE_FORMAT_EXTENSION_CHOICES = (
                                  (PNG_EXTENSION, 'Portable Network Graphics (PNG)'),
                                  (JPEG_EXTENSION, 'Joint Photographic Experts Group picture (JPEG)'),
                                  (JPG_EXTENSION, 'Joint Photographic Experts Group picture (JPG)'),
                                  (BMP_EXTENSION, 'Bitmap Image File (BMP)'),
                                  (TIFF_EXTENSION, 'Tagged Image File Format (TIFF)'),
                                  (GIF_EXTENSION, 'Graphics Interchange Format (GIF)'),
                                  )

# Note: http://www.freeformatter.com/mime-types-list.html
PNG_MIMETYPE = 'image/png'
JPEG_MIMETYPE = 'image/jpeg'
BMP_MIMETYPE = 'image/bmp'
TIFF_MIMETYPE = 'image/tiff'
GIF_MIMETYPE = 'image/gif'
MIMETYPE_CHOICES = (
                    (PNG_MIMETYPE, 'PNG'),
                    (JPEG_MIMETYPE, 'JPEG/JPG'),
                    (BMP_MIMETYPE, 'BMP'),
                    (TIFF_MIMETYPE, 'TIFF'),
                    (GIF_MIMETYPE, 'GIF'),
                    )



class ImageBinaryUpload(models.Model):
    class Meta:
        app_label = 'api'
        db_table = 'ec_image_binary_uploads'
    
    id = models.AutoField(primary_key=True, db_index=True)
    created = models.DateField(auto_now=True, null=True)
    file_type = models.CharField(
        db_index=True,
        max_length=4,
        choices=IMAGE_FORMAT_EXTENSION_CHOICES,
    )
    mime_type = models.CharField(
        db_index=True,
        default=JPEG_MIMETYPE,
        max_length=15,
        choices=MIMETYPE_CHOICES,
    )
    owner = models.ForeignKey(User, null=True)
    data = models.BinaryField()
                                
    def __str__(self):
        return str(self.id)+'.'+str(self.file_type)
    
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
        super(ImageBinary, self).delete(*args, **kwargs) # Call the "real" delete() method

    def save(self, *args, **kwargs):
        """
            Override the save function to reset the cache when a save was made.
        """
        cache = caches['default']
        if cache is not None:
            cache.clear()
            super(ImageBinary, self).save(*args, **kwargs)
