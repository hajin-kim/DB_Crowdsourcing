import os

from django.db import models
from django.conf import settings

# Create your models here.
class OriginFile(models.Model):
    """
    docstring
    """
    # name = models.CharField('파일명', max_length=200)
    file_original = models.FileField('파일', null=True, blank=True, upload_to="data_original/", max_length=100)
    
    def __str__(self):
        """
        docstring
        """
        return self.file_original.name

    def get_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, self.file_original.name)
    

    def delete(self, *args, **kargs):
        if self.file_original:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file_original.name))
        super(OriginFile, self).delete(*args, **kargs)
