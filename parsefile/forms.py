from django import forms

from .models import OriginFile

class UploadForm(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = OriginFile
        # fields = {'name', 'data'}
        fields = {'file_original'}

    def save(self, commit=True):
        self.instance = OriginFile(**self.cleaned_data)
        
        if commit:
            self.instance.save()
            # self.instance.name = self.instance.file_original.name
            # self.instance.save()
        return self.instance


