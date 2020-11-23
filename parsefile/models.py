import os

from django.db import models
from django.conf import settings

from basicdb.models import MappingInfo

# Create your models here.
class OriginFile(models.Model):
    """
    docstring
    """
    # name = models.CharField('파일명', max_length=200)
    derived_schema = models.ForeignKey(MappingInfo, on_delete=models.CASCADE, related_name='file_parsing_schema', verbose_name='파생 스키마')
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
