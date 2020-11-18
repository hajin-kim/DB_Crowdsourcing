from django import forms

from .models import File

class UploadForm(forms.ModelForm):
    """
    docstring
    """
    class Meta:
        model = File
        # fields = {'name', 'data'}
        fields = {'data'}

    def save(self, commit=True):
        self.instance = File(**self.cleaned_data)
        self.instance.name = self.instance.data.name
        if commit:
            self.instance.save()
        return self.instance


