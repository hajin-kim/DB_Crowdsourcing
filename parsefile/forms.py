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
        if commit:
            self.instance.save()
            self.instance.name = self.instance.data.name
            self.instance.save()
        return self.instance


