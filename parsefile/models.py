from django.db import models

# Create your models here.
class File(models.Model):
    """
    docstring
    """
    name = models.CharField('파일명', max_length=200)
    data = models.FileField('파일', null=True, blank=True, upload_to="data_original/", max_length=100)
    
    def __str__(self):
        """
        docstring
        """
        return self.name