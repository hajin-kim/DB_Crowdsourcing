from django import forms

from basicdb.models import Task

class UploadTask(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = Task
        # fields = {'name', 'data'}
        fields = {'name', 'minimal_upload_frequency', 'description', 'original_data_description'}

    # def save(self, commit=True):
    #     self.instance = OriginFile(**self.cleaned_data)
        
    #     if commit:
    #         self.instance.save()
    #         # self.instance.name = self.instance.file_original.name
    #         # self.instance.save()
    #     return self.instance


